from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from main_app.models import Order, OrderItem
from decimal import Decimal
from django.urls import reverse
from django.conf import settings
from .forms import CheckoutForm
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY


def checkout(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_items = OrderItem.objects.filter(order=order)
    sub_order_price = sum(item.quantity * item.product.price for item in order_items)
    tax_rate = Decimal('0.05')
    taxes = sub_order_price * tax_rate
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
    line_items = [
         {
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': 'Total Amount',
                },
                'unit_amount': int(Decimal(price_with_shipping) * 100),
            },
            'quantity': 1,
        }
        for item in order_items
    ]
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        mode='payment',
        success_url=request.build_absolute_uri(reverse('success', args=[order_id])),
        cancel_url=request.build_absolute_uri(reverse('cancel', args=[order_id])),
        client_reference_id=str(price_with_shipping),
        shipping_address_collection=None,
    )
    session_id = session.id
    return redirect(session.url)


def success(request, order_id):
    price_paid = request.GET.get('price_with_shipping')
    context = {
        'order': order_id,
        'price_paid': price_paid,
    }  
    return render(request, 'success.html', context)


def cancel(request, order_id):
    redirect_url = reverse('checkout', args=[order_id])
    return HttpResponseRedirect(redirect_url)
