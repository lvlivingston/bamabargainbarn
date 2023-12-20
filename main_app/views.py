import os
import uuid
import boto3
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
# from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.sessions.models import Session
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.mixins import LoginRequiredMixin
# from .forms import FeedingForm
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_protect
from django.db import transaction
from django.db.models import Sum
from .models import Customer, Product, Order, OrderItem
from django.http import JsonResponse
from django.utils import timezone
from decimal import Decimal
from django.urls import reverse

def products(request):
    # Retrieve products with an inventory of at least 3
    products = Product.objects.filter(inventory__gte=3)
    return render(request, 'products.html', {'products': products})

def cart(request):
    # Ensure the session is created
    if not request.session.session_key:
        request.session.create()

    # Get the current session key
    session_id = request.session.session_key

    # Check if there's an existing order for the current session
    order, created = Order.objects.get_or_create(session_id=session_id, paid=False)

    print("Items in the order:", order.items.all())
    # Your existing code to calculate total_items and update the order

    # Update the URL for the 'checkout' link
    checkout_url = reverse('checkout', args=[order.id])  # Pass order_id as argument

    return render(request, 'cart.html', {'order': order, 'checkout_url': checkout_url})


def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'product.html', {'product': product})


def add_to_cart(request, product_id):
    # Get the product using its id
    product = get_object_or_404(Product, id=product_id)

    # Ensure the session is created
    if not request.session.session_key:
        request.session.create()

    # Get the current session key
    session_id = request.session.session_key

    # Check if there's an existing order for the current session
    order = Order.objects.filter(session_id=session_id, paid=False).first()

    # If an order doesn't exist, create a new one
    if not order:
        order = Order.objects.create(session_id=session_id, paid=False)

    # Check if there's an existing OrderItem for the current product in the order
    order_item = order.items.filter(product=product).first()

    # If the order item doesn't exist, create a new one
    if not order_item:
        order_item = OrderItem(order=order, product=product, quantity=0)

    # Check if the quantity is already 5 or more
    if order_item.quantity >= 5:
        messages.warning(request, "You can only order up to 5 of each item.")
        return redirect('products')

    # Increment the quantity and total_items
    order_item.quantity += 1
    order_item.save()

    order.total_items += 1
    order.save()

    return redirect('cart')


def update_quantity(request, order_item_id):
    order_item = get_object_or_404(OrderItem, id=order_item_id)
    new_quantity = int(request.POST.get('quantity', 0))
    product_inventory = order_item.product.inventory

    if 1 <= new_quantity <= product_inventory:
        # If the new quantity is within the valid range, update the OrderItem
        order_item.quantity = new_quantity
        order_item.save()

        # Recalculate total_items for the associated Order
        order = order_item.order
        order.update_total_items()

        messages.success(request, 'Quantity updated successfully.')
    else:
        messages.error(request, f"We don't have that much in stock. You can choose from 1 and {product_inventory}.")

    return redirect('cart')


def delete_item(request, order_item_id):
    # Get the order item from the database
    order_item = get_object_or_404(OrderItem, id=order_item_id)

    # Get the associated order
    order = order_item.order

    # Delete the order item
    order_item.delete()
    
    # Decrement the total_items in the order by the number in the quantity field
    order.total_items -= order_item.quantity
    order.save()

    return redirect('cart')