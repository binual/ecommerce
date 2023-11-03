from django.db import models
from ecom_adminapp.models import *
from phone_field import PhoneField

class userloginn(models.Model):
  mobile_number = models.CharField(max_length=15, unique=True)

class Cart(models.Model):
    cart_id = models.CharField(max_length=50, blank=True)
    date_added = models.DateField(auto_now_add=True)
    is_active=models.BooleanField(default=True)
    user_login=models.ForeignKey(userloginn,on_delete=models.CASCADE,blank=True,null=True)
    
    
    
class CartItem(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    is_active=models.BooleanField(default=True)
    selected_size = models.ForeignKey(Size, on_delete=models.SET_NULL, null=True) 
    
  
  
    
class Address(models.Model):
    user_login=models.ForeignKey(userloginn,on_delete=models.CASCADE,blank=True,null=True)
    product=models.ForeignKey(Product,on_delete=models.CASCADE,blank=True,null=True)
    fullname = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=20)
    nearest_land_mark= models.CharField(max_length=20)
    date_added = models.DateField(auto_now_add=True)
    
    
    
class Wishlist(models.Model):
    user_login=models.ForeignKey(userloginn,on_delete=models.CASCADE,blank=True,null=True)
    product=models.ForeignKey(Product,on_delete=models.CASCADE,blank=True,null=True)
    added_at = models.DateTimeField(auto_now_add=True)
    
    
    
    
class Payments(models.Model):
    STATUS = (
        ('Paid', 'Paid'),
        ('Cancelled', 'Cancelled'),
    )
    user_login = models.ForeignKey(userloginn, on_delete=models.CASCADE)
    order = models.ForeignKey(Address, on_delete=models.CASCADE, null=True, blank=True)
    selected_size = models.ForeignKey(Size, on_delete=models.SET_NULL, null=True) 
    payment_method = models.CharField(max_length=100)
    amount_paid = models.CharField(max_length=100, null=True, blank=True)
    order_number = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS, default='Paid')