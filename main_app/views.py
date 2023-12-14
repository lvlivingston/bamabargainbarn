import os
import uuid
import boto3
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
# from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.mixins import LoginRequiredMixin
# from .forms import FeedingForm
from django.http import JsonResponse
from .models import Customer, Product, Order, Photo

def deals(request):
    # Fetch all products from the database
    products = Product.objects.all()
    return render(request, 'deals.html', {'products': products})

def cart(request):
    # You can implement your cart logic here to retrieve and display cart items.
    # For a simple example, we'll just retrieve the cart items from the session.

    cart_item_ids = request.session.get('cart', [])
    cart_items = Product.objects.filter(id__in=cart_item_ids)

    # Create a dictionary to store each cart item along with its quantity
    cart_items_with_quantity = {}

    for item in cart_items:
        # Get the quantity of the item from the session
        item_id_str = str(item.id)
        item_quantity = request.session['cart'].get(item_id_str, 0)

        # Add the item and quantity to the dictionary
        cart_items_with_quantity[item] = {
            'quantity': item_quantity,
            'item_id': item.id  # Add item ID for reference in the template
        }

    return render(request, 'cart.html', {'cart_items': cart_items_with_quantity})

def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'product.html', {'product': product})

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # You can implement your cart logic here, for example, using sessions or a dedicated cart model.

    # For a simple example, let's assume we're using sessions to store cart items.
    cart = request.session.get('cart', {})  # Initialize cart as a dictionary
    cart_item_quantity = cart.get(product_id, 0)  # Get the current quantity of the product in the cart
    cart[product_id] = cart_item_quantity + 1  # Add the product to the cart or increment the quantity

    request.session['cart'] = cart

    return redirect('cart')

def increase_quantity(request, product_id):
    if request.method == 'GET':
        quantity = int(request.GET.get('quantity', 1))

        # Ensure 'cart' exists in the session and is a dictionary
        if 'cart' not in request.session or not isinstance(request.session['cart'], dict):
            request.session['cart'] = {}

        # Update the quantity for the specific product
        request.session['cart'][str(product_id)] = quantity
        request.session.modified = True

    # Redirect back to the cart page or refresh the cart section
    return redirect('cart')


def delete_item(request, product_id):
    cart = request.session.get('cart', {})
    
    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session['cart'] = cart
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'error': 'Item not found'}, status=404)


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