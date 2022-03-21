from django.contrib import admin
from .models import Cart, CartItems, Invoice, InvoiceItems, OrderedItems, Orders, Payment

# admin.site.register(Cart)

@admin.register(Cart)
class AdminCart(admin.ModelAdmin):
    list_display = ['user', 'ordered', 'total_price']

@admin.register(CartItems)
class AdminCartItems(admin.ModelAdmin):
    list_display = ['user', 'cart', 'product', 'price', 'quantity']


@admin.register(Orders)
class AdminOrder(admin.ModelAdmin):
    list_display = ['id', 'user', 'ordered', 'total_amount']


@admin.register(OrderedItems)
class AdminOrderItems(admin.ModelAdmin):
    list_display = ['user', 'order', 'product', 'price', 'quantity']


@admin.register(Payment)
class AdminPayment(admin.ModelAdmin):
    list_display = ['order_id', 'payment_method', 'status', 'payment_amount']


@admin.register(Invoice)
class AdminInvoice(admin.ModelAdmin):
    list_display = ['user', 'order_id', 'payment_method', 'payment_status', 'total_amount']



@admin.register(InvoiceItems)
class AdminInvoiceItems(admin.ModelAdmin):
    list_display = ['invoice' ,'product', 'product_pricee']