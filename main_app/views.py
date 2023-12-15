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
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.mixins import LoginRequiredMixin
# from .forms import FeedingForm
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_protect
from django.db import transaction
from .models import Customer, Product, Order, OrderItem
from django.http import JsonResponse

def products(request):
    products = Product.objects.all()
    return render(request, 'products.html', {'products': products})

def cart(request):
    cart_item_ids = request.session.get('cart', [])
    order_token = request.session.get('order_token')

    if order_token:
        order = get_object_or_404(Order, order_token=order_token)
    else:
        # Generate a new order token
        order_token = str(uuid.uuid4())
        request.session['order_token'] = order_token

        # Create a new order
        order = Order.objects.create(order_token=order_token, total_items=0)

    cart_items = order.items.all()
    cart_items_with_quantity = {}

    for item in cart_items:
        cart_items_with_quantity[item.product] = {
            'quantity': item.quantity,
            'item_id': item.product.id,
        }

    return render(request, 'cart.html', {'cart_items': cart_items_with_quantity})

def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'product.html', {'product': product})

@transaction.atomic
@csrf_exempt
@csrf_protect
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Check if an order already exists in the session
    order_token = request.session.get('order_token')

    if not order_token:
        # Generate a unique identifier for the order
        order_token = str(uuid.uuid4())

        # Store the order identifier in the session
        request.session['order_token'] = order_token

        # Create the order with the unique identifier
        order = Order.objects.create(order_token=order_token, total_items=1)  # Initialize total_items with 1
    else:
        # Order already exists, retrieve it from the database
        order = get_object_or_404(Order, order_token=order_token)
        order.total_items += 1  # Increment total_items
        order.save()

    # Associate the product with the order
    order_item, created = order.items.get_or_create(product=product)

    if not created:
        # If the OrderItem already existed, increase the quantity
        order_item.quantity += 1
        order_item.save()

    # Retrieve the cart from the session
    cart = request.session.get('cart', {})

    # Update the cart with the selected product
    cart_item_quantity = cart.get(product_id, 0)
    cart[product_id] = cart_item_quantity + 1
    request.session['cart'] = cart
    request.session.modified = True

    return redirect('cart')

def update_quantity(request, product_id):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        if 'cart' not in request.session or not isinstance(request.session['cart'], dict):
            request.session['cart'] = {}
        request.session['cart'][str(product_id)] = quantity
        request.session.modified = True
        return JsonResponse({'success': True})
    else:
        # Handle other HTTP methods if needed
        return JsonResponse({'success': False, 'error': 'Invalid method'})


def delete_item(request, product_id):
    cart = request.session.get('cart', {})
    str_product_id = str(product_id)

    # Additional debugging statements
    print(f"Attempting to delete item with ID: {str_product_id}")
    print(f"Current Cart: {cart}")

    # Get the order from the session (assuming you store the order ID in the session)
    order_id = request.session.get('order_id')

    try:
        order = Order.objects.get(id=order_id)
        order_item = order.orderitem_set.get(product_id=product_id)

        print(f"OrderItem ID to be deleted: {order_item.id}")
        print(f"OrderItem Quantity before deletion: {order_item.quantity}")

        # Delete the OrderItem
        order_item.delete()

        print(f"OrderItem deleted successfully")

        # Update the total_items in the Order
        order.total_items -= 1
        order.save()

        # Remove the item from the cart session
        del cart[str_product_id]
        request.session['cart'] = cart
        request.session.modified = True

        return JsonResponse({'success': True})
    except Order.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Order not found'}, status=404)
    except OrderItem.DoesNotExist:
        # Additional debugging statement
        print(f"OrderItem not found for product ID: {str_product_id}")
        return


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