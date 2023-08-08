from django.db import models
from django.utils.text import slugify


    
class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50,)
    slug = models.CharField(max_length=50)
    unit = models.CharField(max_length=50)
    description = models.TextField()
    short_description = models.CharField(max_length=255)
    visibility = models.IntegerField()
    publish_date = models.DateTimeField()
    deleted_at = models.DateTimeField(null=True)

class ProductImage(models.Model):
    id = models.AutoField(primary_key=True)
    Product_id = models.IntegerField(default=0)
    image = models.ImageField(upload_to='image/')
    alt = models.CharField(max_length=255, default='') 
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
   
    
class ProductPrice(models.Model):
    id = models.AutoField(primary_key=True)
    Product_id = models.IntegerField(default=0)
    price = models.FloatField() 
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    
class ProductDiscountTax(models.Model):
    id = models.AutoField(primary_key=True)
    Product_id = models.IntegerField(default=0)
    discount = models.FloatField()
    tax = models.FloatField()
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

class ProductUnit(models.Model):
    id = models.AutoField(primary_key=True)
    Product_id = models.IntegerField(default=0)
    units = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

class ProductStock(models.Model):
    id = models.AutoField(primary_key=True)
    Product_id = models.IntegerField(default=0)
    stock = models.IntegerField()
    stockqty = models.IntegerField()
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)  


class ProductVisibility(models.Model):
    id = models.AutoField(primary_key=True)
    Product_id = models.IntegerField(default=0)
    visibility = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)


class ProductStok(models.Model):
    id = models.AutoField(primary_key=True)
    Product_id = models.IntegerField(default=0)
    stock = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)


class Reg(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField()
    phone=models.CharField(max_length=10)
    password=models.CharField(max_length=100)
    confirm_password=models.CharField(max_length=100)


class Log(models.Model):
    userid=models.IntegerField()
    email=models.EmailField()
    password=models.CharField(max_length=100)    
    login_time=models.DateTimeField(auto_now=True)
    ip_address=models.CharField(max_length=100)
    device_name=models.CharField(max_length=100)
    logout_datetime=models.DateTimeField(auto_now=True)
    mac_address=models.CharField(max_length=100)
    osName=models.CharField(max_length=100)


class AddcartProduct(models.Model):
    product_id = models.IntegerField(default=0)
    user_id = models.IntegerField(default=0)
    qty = models.IntegerField()

class Payment(models.Model):
    payment_id = models.CharField(max_length=100)  
    payer_id = models.CharField(max_length=100)
    amount = models.FloatField()  
    status=models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    

class address(models.Model):
    name=models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state=models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    postal_code=models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    

class paydetails(models.Model):
    user_id = models.IntegerField(default=0)
    product_id = models.IntegerField(default=0)  
    tax = models.FloatField()
    discount = models.FloatField()
    qty = models.IntegerField()
    amount = models.FloatField()
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)


    



    
    


    

    

    


        