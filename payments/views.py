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
from main_app.models import Customer, Product, Order, OrderItem
from django.http import JsonResponse
from django.utils import timezone
from decimal import Decimal
from django.urls import reverse
from django.conf import settings
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

def checkout(request, order_id):
    # Get the order for the current session
    order = get_object_or_404(Order, id=order_id)

    # Get all order items for the current order
    order_items = OrderItem.objects.filter(order=order)

    # Calculate the sub_order_price
    sub_order_price = sum(item.quantity * item.product.price for item in order_items)
    taxes = Decimal('3.95')
    price_with_taxes = sub_order_price + taxes
    shipping = Decimal('0.00')
    price_with_shipping = price_with_taxes + shipping

    context = {
        'order': order,
        'order_items': order_items,
        'sub_order_price': sub_order_price,
        'price_with_shipping': price_with_shipping,
    }

    # Pass the context to the render function
    return render(request, 'checkout.html', context)

    
def pay(request, order_id):
    # Construct the line items for the Stripe Checkout Session
    line_items = [
        {
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': item.product.title,
                },
                'unit_amount': int(item.product.price * 100),  # Stripe requires amount in cents
            },
            'quantity': item.quantity,
        }
        for item in order_items
    ]

    # Create a Stripe Checkout Session
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        mode='payment',
        success_url=request.build_absolute_uri(reverse('success', args=[order_id])),
        cancel_url=request.build_absolute_uri(reverse('cancel', args=[order_id])),
    )

    # Extract the session ID
    session_id = session.id

    # Print the session ID to the console
    print(f"Stripe Checkout Session created. Session ID: {session.id}")

    return redirect(session.url)

def success():
    pass

def cancel():
    pass
