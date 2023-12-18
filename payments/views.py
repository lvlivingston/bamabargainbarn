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

def checkout(request, order_id):
    # Get the current session key
    session_id = request.session.session_key

    # Get the order for the current session
    order = Order.objects.filter(session_id=session_id, paid=False).first()

    # Get all order items for the current order
    order_items = OrderItem.objects.filter(order=order)

    # Calculate the sub_order_price
    sub_order_price = sum(item.quantity * item.product.price for item in order_items)
    taxes = Decimal('3.95')
    price_with_taxes = sub_order_price + taxes
    shipping = Decimal('0.00')
    price_with_shipping = price_with_taxes + shipping

    return render(request, 'checkout.html', {'order': order, 'order_items': order_items, 'sub_order_price': sub_order_price, 'price_with_shipping': price_with_shipping})
    
def pay(request, order_id):
    messages.warning(request, "Pay button worked.")
    return redirect('cart')