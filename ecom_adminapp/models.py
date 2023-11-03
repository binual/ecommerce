from django.db import models

# Create your models here.

class Addcategory(models.Model):
    category_name = models.CharField(max_length=200)
    category_image = models.ImageField(upload_to='images/')  



class SubCategory(models.Model):
    category_name = models.ForeignKey(Addcategory, on_delete=models.CASCADE)
    sub_category=models.CharField(max_length=225)
    
    
    
    
class Product(models.Model):
    category_name  =models.ForeignKey(Addcategory, on_delete=models.CASCADE)
    sub_category =models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    title=models.CharField(max_length=500)
    description=models.CharField(max_length=500)
    price= models.IntegerField()
    offer_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # Add the "offer_price" field here
    stock = models.PositiveIntegerField(default=0)  # Add the "stock" field for product quantity
    is_available = models.BooleanField(default=True)  # Add the "is_available" field as a boolean
    offerprice = models.IntegerField()
    
    
    
class Image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/')
    
    
    
    
class Size(models.Model):
    name = models.CharField(max_length=50)
    
class ProductSize(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)


class Color(models.Model):
    name = models.CharField(max_length=50)
    
class ProductColor(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
