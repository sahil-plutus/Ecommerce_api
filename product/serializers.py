from rest_framework import serializers
from .models import *



class QuantitySerializer(serializers.ModelSerializer):
    class Meta:
        model = QuantityVariant
        fields = '__all__'


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ColorVariant
        fields = '__all__'


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SizeVariant
        fields = '__all__'


class CatagorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Catagory
        fields = '__all__'
        

class ProductSerializer(serializers.ModelSerializer):
    catagory = CatagorySerializer()
    quantity_type = QuantitySerializer()
    color_type = ColorSerializer()
    size_type = SizeSerializer()
    class Meta:
        model = Product
        fields = '__all__'


class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

    class Meta:
        fields = ('file',)