from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=250)
    category = models.CharField(max_length=20)
    image = models.ImageField()
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    totalRating = models.IntegerField()

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
    
    products = models.ManyToManyField(Product)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('profile', kwargs={'customer_id': self.id})
    
    # def fed_for_today(self):
    #     return self.feeding_set.filter(date=date.today()).count() >= len(MEALS)

# Add new Feeding model below Cat model
class Order(models.Model):
    date = models.DateField('Order Placed')
    totalItems = models.IntegerField()
    products = models.ManyToManyField(Product)

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        # Nice method for obtaining the friendly value of a Field.choice
        return f"Order on {self.date}"
    
    # change the default sort
    class Meta:
        ordering = ['-date']

class Photo(models.Model):
    url = models.CharField(max_length=200)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for product_id: {self.product_id} @{self.url}"

