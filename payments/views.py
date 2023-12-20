import os
import uuid
import boto3
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
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
from django import forms
from .forms import CheckoutForm
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

def checkout(request, order_id):
    # Get the order for the current session
    order = get_object_or_404(Order, id=order_id)

    # Get all order items for the current order
    order_items = OrderItem.objects.filter(order=order)

    # Calculate the sub_order_price
    sub_order_price = sum(item.quantity * item.product.price for item in order_items)
    # Set the tax rate (5% in this example)
    tax_rate = Decimal('0.05')
    # Calculate taxes
    taxes = sub_order_price * tax_rate
    # Assuming you want to include taxes in the final price
    price_with_taxes = sub_order_price + taxes
    shipping = Decimal('0.00')
    price_with_shipping = price_with_taxes + shipping

    order.price_with_shipping = price_with_shipping
    order.save()

    context = {
        'order': order,
        'order_items': order_items,
        'sub_order_price': sub_order_price,
        'price_with_shipping': price_with_shipping,
    }

    # Pass the context to the render function
    return render(request, 'checkout.html', context)

    
def pay(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_items = OrderItem.objects.filter(order=order)

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order.first_name = form.cleaned_data['first_name']
            order.last_name = form.cleaned_data['last_name']
            order.street_address = form.cleaned_data['street_address']
            order.city = form.cleaned_data['city']
            order.state = form.cleaned_data['state']
            order.ship_zip = form.cleaned_data['ship_zip']
            order.save()
        else:
            form = CheckoutForm()
    else:
        form = CheckoutForm()

    price_with_shipping = order.price_with_shipping

    # Construct the line items for the Stripe Checkout Session
    line_items = [
         {
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': 'Total Amount',  # You can customize this label
                },
                'unit_amount': int(Decimal(price_with_shipping) * 100),  # Stripe requires amount in cents
            },
            'quantity': 1,  # Quantity is 1 for the total amount
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
        client_reference_id=str(price_with_shipping),
        shipping_address_collection=None,
    )

    # Extract the session ID
    session_id = session.id

    # Print the session ID to the console
    print(f"Stripe Checkout Session created. Session ID: {session.id}")

    return redirect(session.url)


def success(request, order_id):
    
    # Retrieve price_with_shipping from URL parameters
    price_with_shipping = request.GET.get('price_with_shipping')

    context = {
        'order': order_id,
        'price_with_shipping': price_with_shipping,
    }
        
    return render(request, 'success.html', context)

def cancel(request, order_id):
    # You can customize the URL to redirect to
    redirect_url = reverse('checkout', args=[order_id])
    
    return HttpResponseRedirect(redirect_url)
