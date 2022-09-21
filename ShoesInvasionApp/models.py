from configparser import MAX_INTERPOLATION_DEPTH
from datetime import date
from operator import length_hint
from tkinter import CASCADE
from turtle import color
from unittest.util import _MAX_LENGTH
from django.db import models

# Create your models here.

# Users Table
class users(models.Model):
    user_id = models.IntegerField(default=0, primary_key=True)
    fname = models.CharField(max_length=45)
    lname = models.CharField(max_length=45)
    address = models.TextField(default="")
    email = models.CharField(max_length=255)
    dob = models.DateField(default=date.today)
    gender = models.CharField(max_length=1)
    user_username = models.CharField(max_length=255)
    user_password = models.CharField(max_length=255)
    forget_pwd_code = models.CharField(max_length=10)
    phone = models.IntegerField(default=0)
    banned_status = models.CharField(max_length=1)

# Admin Users Table
class admin_users(models.Model):
    admin_user_id = models.IntegerField(default=0, primary_key=True)
    admin_username = models.CharField(max_length=255)
    admin_password = models.CharField(max_length=255)

# Transactions Table
class transactions(models.Model):
    transaction_id = models.IntegerField(default=0, primary_key=True)
    createdDate = models.DateField(default=date.today)
    user_id = models.ForeignKey(users, on_delete=models.CASCADE)

# Products Table
class products(models.Model):
    product_id = models.IntegerField(primary_key=True)
    product_name = models.CharField(max_length=45)
    product_price = models.DecimalField(default=0, decimal_places=2, max_digits=6)
    review = models.TextField(default="")
    product_info = models.TextField(default="")
    product_brand = models.CharField(max_length=45)
    product_category = models.CharField(max_length=45)
    gender_type = models.CharField(max_length=1)
    available = models.CharField(max_length=3)

# Transaction Details Table
class transaction_details(models.Model):
    transaction_details_id = models.IntegerField(default=0, primary_key=True)
    transaction = models.ForeignKey(transactions, on_delete=models.CASCADE)
    product = models.ForeignKey(products, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    size = models.CharField(max_length=5)
    amount = models.DecimalField(default=0, decimal_places=2, max_digits=6)

# Products Quantity Table
class product_quantity(models.Model):
    product = models.ForeignKey(products, on_delete=models.CASCADE)
    size = models.CharField(max_length=5)
    quantity = models.IntegerField(default=0)
    color = models.CharField(max_length=45)

# Shopping Cart Table
class Shopping_Cart(models.Model):
    shopping_id = models.IntegerField(default=0, primary_key=True)
    user = models.ForeignKey(users, on_delete = models.CASCADE)
    product_id = models.IntegerField(default=0)
    quantity = models.IntegerField(default=0)
    size = models.CharField(max_length=5)
    color = models.CharField(max_length=45)
    total_price = models.DecimalField(default=0, decimal_places=2, max_digits=6)
    status = models.CharField(max_length=20)
