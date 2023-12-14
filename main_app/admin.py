from django.contrib import admin
from .models import Customer, Order, Product, OrderItem

if not admin.site.is_registered(Customer):
    admin.site.register(Customer)

if not admin.site.is_registered(Order):
    admin.site.register(Order)

if not admin.site.is_registered(Product):
    admin.site.register(Product)

if not admin.site.is_registered(OrderItem):
    admin.site.register(OrderItem)