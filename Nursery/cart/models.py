from django.contrib.auth.models import User
from django.db import models
from home.models import *
from account.models import *

# Create your models here.
class cartlist(models.Model):
    cart_id=models.CharField(max_length=250,unique=True)
    date_added=models.DateTimeField(auto_now_add=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,default=None)

    def __str__(self):
        return self.cart_id

class items(models.Model):
    plant_obj=models.ForeignKey(add_plants,on_delete=models.CASCADE)
    cart=models.ForeignKey(cartlist,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    active=models.BooleanField(default=True)

    def __str__(self):
        return str(self.plant_obj)
    def total(self):
        return self.plant_obj.price*self.quantity

class Checkout(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    cart=models.ForeignKey(cartlist,on_delete=models.CASCADE,null=True)
    firstname=models.CharField(max_length=100)
    lastname=models.CharField(max_length=100)
    country=models.CharField(max_length=100)
    state=models.CharField(max_length=100)
    address=models.TextField(max_length=200)
    towncity=models.CharField(max_length=100)
    postcodezip=models.CharField(max_length=50)
    phone=models.CharField(max_length=20)

    email=models.EmailField()

class payment(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    account_number=models.CharField(max_length=200)
    name=models.CharField(max_length=100)
    expiry_month=models.CharField(max_length=2)
    expiry_year=models.CharField(max_length=2)
    cvv=models.CharField(max_length=3)
    def __str__(self):

        return self.name


class OrderManagement(models.Model):
    customer_checkout = models.ForeignKey(Checkout, on_delete=models.CASCADE)
    order_item = models.ForeignKey(items, on_delete=models.CASCADE)
    order_date =models.DateTimeField(auto_now_add=True)
    plant = models.ForeignKey(add_plants, on_delete=models.CASCADE,default='')


    def __str__(self):
        return f"Order for {self.customer_checkout.user.username} - {self.order_date}"
