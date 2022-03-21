from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from product.models import Product
from django.db.models.signals import pre_save, post_save


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)

    def _get_total_price(self):
        sub_total = 0
        for i in self.cart_items.all():
            sub_total += i.price
        return sub_total
    total_price = property(_get_total_price)

    def __str__(self):
        return str(self.user)


class CartItems(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.FloatField(default=0)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return str(self.user.username) + " " + str(self.product.product_name)


@receiver(pre_save, sender = CartItems)
def correct_price(sender, **kwargs):
    cart_items = kwargs['instance']
    price_of_product = Product.objects.get(id = cart_items.product.id)
    cart_items.price =  cart_items.quantity * float(price_of_product.price)
    total_cart_items = CartItems.objects.filter(cart = cart_items.cart)
    cart_items.total_items = len(total_cart_items)




Ordered =((True, 'Successfull'), (False,'Pending'))

class Orders(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(choices=Ordered, default=False)
    shipping_charges = models.IntegerField(default=70)
    total_amount = models.FloatField(blank=True)

    def save(self, *args, **kwargs):
        total_price = Cart.objects.get(user = self.user)
        if self.total_amount:
            self.total_amount = (self.total_amount + self.shipping_charges)
        return super().save()



class OrderedItems(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="order_items")
    price = models.FloatField(default=0)
    quantity = models.IntegerField(default=1)
    def __str__(self):
        return f"{self.user} - {self.product} - {self.order.id}"



STATUS = (
    ('cash on delevery', 'cash on delevery'),
    ('Stripe', 'Stripe'),
)

PAYMENT_STATUS = (
    ('Draft', 'Draft'),
    ('Pending', 'Pending'),
    ('Done', 'Done'),
)


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_id = models.ForeignKey(Orders, on_delete=models.PROTECT, related_name="payment_ids")
    payment_method = models.CharField(choices=STATUS, max_length=22)
    status = models.CharField(choices=PAYMENT_STATUS, max_length=22, default="Draft")
    payment_amount = models.IntegerField()
    order_secret_id = models.CharField(max_length=122, blank=True)

    def save(self, *args, **kwargs):
        order = Orders.objects.get(id = self.order_id.id)
        self.payment_amount = order.total_amount
        return super().save()


class Invoice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=122)
    payment_method = models.CharField(max_length=122)
    payment_status = models.CharField(max_length=122)
    total_amount = models.FloatField(max_length=122)
    shipping_charge = models.FloatField(default=70.00)


class InvoiceItems(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete = models.CASCADE)
    product = models.ForeignKey(Product ,on_delete = models.CASCADE, related_name="invoice_product")
    product_pricee = models.FloatField(default= 0)