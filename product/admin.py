from django.contrib import admin
from .models import ColorVariant, Product, Catagory, QuantityVariant, SizeVariant

admin.site.register(Product)
admin.site.register(Catagory)
admin.site.register(QuantityVariant)
admin.site.register(ColorVariant)
admin.site.register(SizeVariant)
