from django.db import models
from django.contrib.auth.models import AbstractUser
from inventory.managers import CustomUserManager
# Create your models here.



class CustomUser(AbstractUser):
    Username = None
    email = models.EmailField(unique=True)
    Phone = models.CharField(max_length=14, blank=True, null=True)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()
    
    def __str__(self):
        return self.email
    
    
class UserProfile(models.Model):
    id = models.BigIntegerField(auto_created=True, primary_key=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='Profile')
    address = models.TextField(max_length=250)
    city = models.TextField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username}'s profile"
    
class CustomerCategory(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
class Customer(models.Model):
    id = models.BigIntegerField(auto_created=True, primary_key=True)
    name = models.CharField(max_length=200)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20)
    address = models.TextField(blank=True)
    category = models.ForeignKey(CustomerCategory, on_delete=models.SET_NULL, blank=True, null=True, related_name='Cutomer')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class Product(models.Model):
    id = models.BigIntegerField(auto_created=True, primary_key=True)
    name = models.CharField(max_length=250)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(blank=True, null=True)
    active = models.BooleanField(default=True)
    category = models.ForeignKey(CustomerCategory, on_delete=models.SET_NULL, blank=True, null=True, related_name='product')
    create_at =models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
class Invoice(models.Model):
    id = models.BigIntegerField(auto_created=True, primary_key=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='invoice')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=12, decimal_places=2)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True, related_name='invoice')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=True, null=True, related_name='invoice')
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.id
    