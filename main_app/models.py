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
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    street_address = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=25, blank=True, null=True)
    state = models.CharField(max_length=2, blank=True, null=True)
    zip_code = models.CharField(max_length=5, blank=True, null=True)
    email = models.EmailField(max_length=75, blank=True, null=True)
    phone = models.CharField(max_length=10, blank=True, null=True)
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    def get_absolute_url(self):
        return reverse('profile', kwargs={'customer_id': self.id})
    
    
class Order(models.Model):
    csrf_token = models.CharField(max_length=256, blank=True, null=True, unique=True)
    session_id = models.CharField(max_length=256, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    date = models.DateField('Order Placed', default=timezone.now)  # Use default to set the current time
    total_items = models.IntegerField(default=0)
    paid = models.BooleanField(default=False)
    price_with_shipping = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=None)
    price_paid = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=None)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    street_address = models.TextField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=25, blank=True, null=True)
    state = models.TextField(max_length=2, blank=True, null=True)
    ship_zip = models.CharField(max_length=5, blank=True, null=True)
    email = models.EmailField(max_length=75, blank=True, null=True)
    phone = models.CharField(max_length=10, blank=True, null=True)
    bil_zip = models.CharField(max_length=5, blank=True, null=True)
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    def update_total_items(self):
        self.total_items = sum(item.quantity for item in self.items.all())
        self.save()
    def get_absolute_url(self):
        return reverse('checkout', args=[str(self.id)])
    def orderSubtotal(self):
        return sum(item.sub_item_price for item in self.items.all())
    def __str__(self):
        return f"Order on {self.date}"
    class Meta:
        ordering = ['-date']


class OrderItem(models.Model):
    csrf_token = models.CharField(max_length=256, blank=True, null=True, unique=True)
    session_id = models.CharField(max_length=256, blank=True, null=True)
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    sub_item_price = models.DecimalField(max_digits=10, decimal_places=2)
    def save(self, *args, **kwargs):
        self.subtotal = self.product.price * self.quantity
        self.sub_item_price = self.subtotal
        super(OrderItem, self).save(*args, **kwargs)
    def __str__(self):
        return f"{self.quantity} of {self.product.title} in Order {self.order.date}"

