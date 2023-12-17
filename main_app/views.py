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
    order = order_item.order
    new_quantity = int(request.POST.get('quantity', 0))
    product_inventory = order_item.product.inventory

    if 1 <= new_quantity <= product_inventory:
        # If the new quantity is within the valid range, update the OrderItem
        order_item.quantity = new_quantity
        order_item.save()
        messages.success(request, 'Quantity updated successfully.')
    else:
        messages.error(request, f"We don't have that much in stock. You can choose from 1 and {product_inventory}.")

    return redirect('cart')


def delete_item(request, order_item_id):
    # Get the order item from the database
    order_item = get_object_or_404(OrderItem, id=order_item_id)

    # Get the associated order
    order = order_item.order

    # Decrement the total_items in the order by the number in the quantity field
    order.total_items -= order_item.quantity
    order.save()

    # Delete the order item
    order_item.delete()

    return redirect('cart')

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

# @login_required
# def finches_index(request):
#   finches = Finch.objects.filter(user=request.user)
#   # You could also retrieve the logged in user's cats like this
#   # cats = request.user.cat_set.all()
#   return render(request, 'finches/index.html', { 'finches': finches })

# @login_required
# def finches_detail(request, finch_id):
#     finch = Finch.objects.get(id=finch_id)
#     id_list = finch.toys.all().values_list('id')
#     toys_finch_doesnt_have = Toy.objects.exclude(id__in=id_list)
#     feeding_form = FeedingForm()
#     return render(request, 'finches/detail.html', {
#         'finch': finch, 
#         'feeding_form': feeding_form,
#         # Add the toys to be displayed
#         'toys': toys_finch_doesnt_have
#     })

# class FinchCreate(LoginRequiredMixin, CreateView):
#   model = Finch
#   fields = ['name', 'scientificname', 'mass', 'description', 'diet']

#   # This inherited method is called when a
#   # valid cat form is being submitted
#   def form_valid(self, form):
#     # Assign the logged in user (self.request.user)
#     form.instance.user = self.request.user  # form.instance is the cat
#     # Let the CreateView do its job as usual
#     return super().form_valid(form)

# class FinchUpdate(LoginRequiredMixin, UpdateView):
#   model = Finch
#   fields = ['scientificname', 'mass', 'description', 'diet']

# class FinchDelete(LoginRequiredMixin, DeleteView):
#   model = Finch
#   success_url = '/finches'

# @login_required
# def add_feeding(request, finch_id):
#   # create a ModelForm instance using the data in request.POST
#   form = FeedingForm(request.POST)
#   # validate the form
#   if form.is_valid():
#     # don't save the form to the db until it
#     # has the finch_id assigned
#     new_feeding = form.save(commit=False)
#     new_feeding.finch_id = finch_id
#     new_feeding.save()
#   return redirect('detail', finch_id=finch_id)

# class ToyList(LoginRequiredMixin, ListView):
#   model = Toy

# class ToyDetail(LoginRequiredMixin, DetailView):
#   model = Toy

# class ToyCreate(LoginRequiredMixin, CreateView):
#   model = Toy
#   fields = '__all__'

# class ToyUpdate(LoginRequiredMixin, UpdateView):
#   model = Toy
#   fields = ['name', 'color']

# class ToyDelete(LoginRequiredMixin, DeleteView):
#   model = Toy
#   success_url = '/toys'

# @login_required
# def assoc_toy(request, finch_id, toy_id):
#   # Note that you can pass a toy's id instead of the whole toy object
#   Finch.objects.get(id=finch_id).toys.add(toy_id)
#   return redirect('detail', finch_id=finch_id)

# @login_required
# def unassoc_toy(request, finch_id, toy_id):
#   Finch.objects.get(id=finch_id).toys.remove(toy_id)
#   return redirect('detail', finch_id=finch_id)

# @login_required
# def add_photo(request, finch_id):
#     # photo-file will be the "name" attribute on the <input type="file">
#     photo_file = request.FILES.get('photo-file', None)
#     if photo_file:
#         s3 = boto3.client('s3')
#         # need a unique "key" for S3 / needs image file extension too
#         key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
#         # just in case something goes wrong
#         try:
#             bucket = os.environ['S3_BUCKET']
#             s3.upload_fileobj(photo_file, bucket, key)
#             # build the full url string
#             url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
#             # we can assign to cat_id or cat (if you have a cat object)
#             Photo.objects.create(url=url, finch_id=finch_id)
#         except Exception as e:
#             print('An error occurred uploading file to S3')
#             print(e)
#     return redirect('detail', finch_id=finch_id)

# def signup(request):
#   error_message = ''
#   if request.method == 'POST':
#     # This is how to create a 'user' form object
#     # that includes the data from the browser
#     form = UserCreationForm(request.POST)
#     if form.is_valid():
#       # This will add the user to the database
#       user = form.save()
#       # This is how we log a user in via code
#       login(request, user)
#       return redirect('index')
#     else:
#       error_message = 'Invalid sign up - try again'
#   # A bad POST or a GET request, so render signup.html with an empty form
#   form = UserCreationForm()
#   context = {'form': form, 'error_message': error_message}
#   return render(request, 'registration/signup.html', context)