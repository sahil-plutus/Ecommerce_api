from django.db import models
from django.utils.text import slugify
from django.core.validators import FileExtensionValidator



class Catagory(models.Model):
    catagory_name = models.CharField(max_length=122)
    slug = models.SlugField(max_length=122, blank=True)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.catagory_name)
        return super().save()

    def __str__(self):
        return self.catagory_name



class QuantityVariant(models.Model):
    variant_name = models.CharField(max_length=122)
    
    def __str__(self):
        return self.variant_name


class ColorVariant(models.Model):
    color_name = models.CharField(max_length=122)
    
    def __str__(self):
        return self.color_name


class SizeVariant(models.Model):
    size_name = models.CharField(max_length=122)
    
    def __str__(self):
        return self.size_name


class Product(models.Model):
    catagory = models.ForeignKey(Catagory, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=122)
    image = models.ImageField(upload_to = 'media/products')
    price = models.CharField(max_length=20)
    description = models.TextField()
    stock = models.IntegerField(default=100)

    quantity_type = models.ForeignKey(QuantityVariant, blank=True, null=True, on_delete=models.PROTECT)
    color_type = models.ForeignKey(ColorVariant, blank=True, null=True, on_delete=models.PROTECT)
    size_type = models.ForeignKey(SizeVariant, blank=True, null=True, on_delete=models.PROTECT)

    def __str__(self):
        return self.product_name


class ProductImages(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    image = models.ImageField(upload_to = "media/products")

