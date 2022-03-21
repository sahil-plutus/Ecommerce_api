from rest_framework import serializers
from .models import *
from product.serializers import *



class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'

class CartItemsSerializer(serializers.ModelSerializer):
    cart = CartSerializer()
    product = ProductSerializer()
    class Meta:
        model = CartItems
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    # cart = CartSerializer()
    class Meta:
        model = Orders
        fields = '__all__'

    
class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'
