from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import date
from django.utils import timezone

class Product(models.Model):
    title = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=250)
    category = models.CharField(max_length=20)
    image = models.ImageField(upload_to='static/images/', blank=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    totalRating = models.IntegerField()
    is_available = models.BooleanField(default=True)
    inventory = models.PositiveIntegerField(default=3)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'pk': self.id})
    

class Customer(models.Model):
    name = models.CharField(max_length=50)
    firstName = models.CharField(max_length=25)
    lastName = models.CharField(max_length=25)
    email = models.EmailField(max_length=75)
    streetAddress = models.TextField(max_length=100)
    city = models.CharField(max_length=25)
    state = models.TextField(max_length=2)
    zip = models.CharField(max_length=25)
    phone = models.CharField(max_length=10)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('profile', kwargs={'customer_id': self.id})
    
    
class Order(models.Model):
    csrf_token = models.CharField(max_length=255, blank=True, null=True, unique=True)
    session_id = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    date = models.DateField('Order Placed', default=timezone.now)  # Use default to set the current time
    total_items = models.IntegerField(default=0)
    paid = models.BooleanField(default=False)
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Order on {self.date}"

    class Meta:
        ordering = ['-date']


class OrderItem(models.Model):
    csrf_token = models.CharField(max_length=255, blank=True, null=True, unique=True)
    session_id = models.CharField(max_length=255, blank=True, null=True)
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.product.title} in Order {self.order.date}"

