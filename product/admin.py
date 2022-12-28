from django.contrib import admin
from .models import Product, Productoffer, Categoryoffer

admin.site.register(Product)
admin.site.register(Categoryoffer)
admin.site.register(Productoffer)

