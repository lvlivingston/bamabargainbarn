from django.contrib import admin
from .models import Customer, Order, Product, Photo

if not admin.site.is_registered(Customer):
    admin.site.register(Customer)

if not admin.site.is_registered(Order):
    admin.site.register(Order)

if not admin.site.is_registered(Product):
    admin.site.register(Product)

if not admin.site.is_registered(Photo):
    admin.site.register(Photo)