from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Product, Order, OrderItem
from django.urls import reverse


def products(request):
    products = Product.objects.filter(inventory__gte=3)
    return render(request, 'products.html', {'products': products})


def cart(request):
    if not request.session.session_key:
        request.session.create()
    session_id = request.session.session_key
    order, created = Order.objects.get_or_create(session_id=session_id, paid=False)
    checkout_url = reverse('checkout', args=[order.id])
    return render(request, 'cart.html', {'order': order, 'checkout_url': checkout_url})


def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'product.html', {'product': product})


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product_inventory = product.inventory
    if not request.session.session_key:
        request.session.create()
    session_id = request.session.session_key
    order = Order.objects.filter(session_id=session_id, paid=False).first()
    if not order:
        order = Order.objects.create(session_id=session_id, paid=False)
    order_item = order.items.filter(product=product).first()
    if not order_item:
        order_item = OrderItem(order=order, product=product, quantity=0)
    if order_item.quantity >= product_inventory:
        messages.warning(request, f"We only have {product_inventory} left in stock.")
        return redirect('products')
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
        order_item.quantity = new_quantity
        order_item.save()
        order = order_item.order
        order.update_total_items()
        messages.success(request, 'Quantity updated successfully.')
    else:
        messages.error(request, f"We don't have that much in stock. You can choose from 1 and {product_inventory}.")
    return redirect('cart')


def delete_item(request, order_item_id):
    order_item = get_object_or_404(OrderItem, id=order_item_id)
    order = order_item.order
    order_item.delete()
    order.total_items -= order_item.quantity
    order.save()
    return redirect('cart')