from django.shortcuts import render, HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Cart, CartItems, Product, Orders, Invoice
from .serializers import *
import stripe
from django.utils.decorators import method_decorator
import json
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.http import JsonResponse
from django.template.loader import get_template
from django.core.mail import EmailMessage
from io import BytesIO
from xhtml2pdf import pisa
import os
from django.views.generic import View


stripe.api_key = settings.STRIPE_SECRETE_KEY

endpoint_secret = settings.STRIPE_WEBHOOK_SECRETE


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return result.getvalue()
    return None



class CartView(APIView):
    # permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        cart = Cart.objects.filter(user = user, ordered = False).first()
        queryset = CartItems.objects.filter(cart = cart)
        serializer = CartItemsSerializer(queryset, many = True)
        return Response(serializer.data)


    def post(self, request):
        data = request.data
        user = request.user
        cart,_ = Cart.objects.get_or_create(user = user, ordered = False)
        product = Product.objects.get(product_name = data.get('product_name'))
        price = product.price
        quantity = data.get('quantity')
        cart_items = CartItems( cart = cart, user = user, product = product, quantity = quantity)
        cart_items.save()
        return Response({'success':'Items Added in your cart'})


    def put(self, request):
        data = request.data
        print(data)
        product = Product.objects.get(product_name = data['product_name'])
        cart_item = CartItems.objects.get(product = product)
        quantity = data.get('quantity')
        cart_item.quantity += quantity
        cart_item.save()
        return Response({'success':'Item Updated'})


    def delete(self, request):
        user = request.user
        data = request.data
        product = Product.objects.get(product_name = data['product_name'])
        cart_item = CartItems.objects.get(product = product)
        cart_item.delete()
        return Response({"msg":"Your Product is delete successfully on your cart!"})


class OrderAPI(APIView):
    def get(self, request):
        queryset = Orders.objects.filter(user = request.user)
        serializer = OrderSerializer(queryset, many = True)
        return Response(serializer.data)

    def post(self, request):
        user = request.user
        data = request.data
        cart = Cart.objects.get(user = request.user)
        cart_items = CartItems.objects.filter(cart = cart)
        if cart.total_price > 70:
            order = Orders(user = user, total_amount = cart.total_price)
            order.save()
        else:
            return Response({'error':'please add a product in cart'})

        for item in cart_items:
            OrderedItems.objects.create(user = request.user ,product=item.product, price= item.price, quantity = item.quantity, order=order)

        for item in cart_items:
            item.delete()
        return Response({"order_id": order.id , "order_amount":order.total_amount})



class PaymentAPI(APIView):
    def get(self, request):
        payment = Payment.objects.filter(user = request.user)
        serializer = PaymentSerializer(payment, many = True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        order = Orders.objects.get(pk=data['order_id'])
        YOUR_DOMAIN = "http://127.0.0.1:8000/api/"
        paymnt = Payment.objects.filter(order_id = order)
        secrete_id_exist = Payment.objects.filter(order_secret_id = '')

        if paymnt.exists():
            return Response({'Payment Already Created'})
        
        else:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types = ['card'],
                line_items = [
                    {
                        'price_data':{'currency':'inr',
                                    'unit_amount': int(order.total_amount * 100), 
                                    'product_data':{'name':order.user.username}},
                        'quantity':1,
                    },
                ],
                metadata = {"order_id":order.id},
                mode = "payment",
                success_url = YOUR_DOMAIN + "payment_success",
                cancel_url = YOUR_DOMAIN + "payment_cancel",
            )
            payment = Payment.objects.create(user = request.user,payment_method=data['payment_method'],order_id=order, status = "Done")
            order.ordered = True
            order.save()
            return Response({'url':checkout_session.url}) 



@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRETE
        )

    except ValueError as e:
        return HttpResponse(status=400)


    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']['metadata']['order_id']
        print('-------------------------------------------', session)
        payment = Payment.objects.get(order_id = session)
        if payment:
            payment.order_secret_id = event['data']['object']['payment_intent']
            payment.save()
        
    return HttpResponse(status=200)


class PaymentSuccess(APIView):
    def get(self, request):
        return Response({'msg','Your Payment has been succeed'})


class PaymentCancel(APIView):
    def get(self, request):
        return Response({'msg','Your Payment has cancel'})


class ShowInvoice(APIView):
    def post(self, request, *args, **kwargs):
        template = get_template('index.html')
        data = request.data
        order_id = data['order_id']
        Order = Orders.objects.get(id = order_id)
        payment = Payment.objects.get(order_id = Order)
        user = Order.user
        orderitems = OrderedItems.objects.filter(order = Order)
        pdf = render_to_pdf('index.html', {'order_items':orderitems, 'payment':payment, 'user':user, 'order':Order})
        return HttpResponse(pdf, content_type = 'application/pdf')


class DownloadInvoice(APIView):
    def post(self, request):
        template = get_template('index.html')
        data = request.data
        order_id = data['order_id']
        Order = Orders.objects.get(id = order_id)
        payment = Payment.objects.get(order_id = Order)
        user = Order.user
        invoice = Invoice(user = user, order_id = order_id, payment_method = payment.payment_method, payment_status = payment.status, total_amount = payment.payment_amount)
        invoice.save()
        orderitems = OrderedItems.objects.filter(order = Order)
        for i in orderitems:
            InvoiceItems.objects.create(invoice = invoice, product = i.product, product_pricee = i.price)
        
        pdf = render_to_pdf('index.html', {'invoice':invoice, 'order_items':orderitems, 'payment':payment, 'user':user, 'order':Order})

        if pdf:
            response = HttpResponse(pdf, content_type = 'application/pdf')
            filename = "Invoice_%s.pdf" %(data['order_id'])
            content = "inline; filename = '%s'" %(filename)
            content = "attachment; filename = '%s'" %(filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("not found")



class ShareInvoice(APIView):
    def post(self, request):
        template = get_template('index.html')
        data = request.data
        order_id = data['order_id']
        Order = Orders.objects.get(id = order_id)
        payment = Payment.objects.get(order_id = Order)
        user = Order.user
        invoice = Invoice(user = user, order_id = order_id, payment_method = payment.payment_method, payment_status = payment.status, total_amount = payment.payment_amount)
        invoice.save()
        orderitems = OrderedItems.objects.filter(order = Order)
        for i in orderitems:
            InvoiceItems.objects.create(invoice = invoice, product = i.product, product_pricee = i.price)
        
        pdf = render_to_pdf('index.html', {'invoice':invoice, 'order_items':orderitems, 'payment':payment, 'user':user, 'order':Order})

        if pdf:
            filename = "Invoice.pdf"
            content = "attachment; filename = '%s'" %(filename)
            mail_subject = "Recent Order Details"
            email = EmailMessage(mail_subject, 'this is a message', settings.EMAIL_HOST_USER, [user.email])
            email.attach('new.pdf', pdf, "application/pdf")
            email.send()
        return Response({'msg':'Invoice generated!'})

