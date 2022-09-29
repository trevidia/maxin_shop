from django.contrib import admin

# Register your models here.
from .models import Products, Size, Order, Cart

admin.site.register(Products)
admin.site.register(Size)
admin.site.register(Cart)
admin.site.register(Order)
