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
from .models import Customer, Product, Order, OrderItem
from django.http import JsonResponse
from django.utils import timezone

def products(request):
    products = Product.objects.all()
    return render(request, 'products.html', {'products': products})

def cart(request):
    # Ensure the session is created
    if not request.session.session_key:
        request.session.create()

    # Get the current session key
    session_id = request.session.session_key

    # Get or create the order for the current session
    order, created = Order.objects.get_or_create(session_id=session_id, paid=False)

    return render(request, 'cart.html', {'order': order})

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

    # Increment the quantity and total_items
    order_item.quantity += 1
    order_item.save()

    order.total_items += 1
    order.save()

    return redirect('cart')








    # if not order_token:
    #     # Generate a unique identifier for the order
    #     order_token = str(uuid.uuid4())

    #     # Store the order identifier in the session
    #     request.session['order_token'] = order_token

    #     # Create the order with the unique identifier
    #     order = Order.objects.create(order_token=order_token, total_items=1)  # Initialize total_items with 1
    #     orderItem = OrderItem.objects.create(order_token=order_token, quantity=1)
    # else:
    #     # Order already exists, retrieve it from the database
    #     order = get_object_or_404(Order, order_token=order_token)
    #     orderItem = get_object_or_404(OrderItem, order_token=order_token)
    #     order.total_items += 1  # Increment total_items
    #     orderItem.quantity += 1  # Increment total_items
    #     order.save()
    #     orderItem.save()

    # # Retrieve the cart from the session
    # cart = request.session.get('cart', {})

    # # Update the cart with the selected product
    # cart_item_quantity = cart.get(product_id, 0)
    # cart[product_id] = cart_item_quantity + 1
    # request.session['order_token'] = order_token
    # request.session.modified = True

    # return redirect('cart')

def update_quantity(request, product_id, orderitem_id):
    order_token = request.session.get('order_token')

    if request.method == 'POST':
        orderitem_id = request.POST.get('orderitem_id')
        quantity = int(request.POST.get('orderitem_id.quantity', 1))
        order_item = get_object_or_404(OrderItem, orderitem__id=orderitem_id, product__id=product_id)


        # Check if there is an active order for the session
        if 'order_token' in request.session:
            order_token = request.session['order_token']
            request.session['order_token'] = order_token
            request.session.modified = True
            # If the order item already exists, update the quantity
            if not created:
                order_item.quantity = quantity
                order_item.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'No active order'})
            return redirect('cart')
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