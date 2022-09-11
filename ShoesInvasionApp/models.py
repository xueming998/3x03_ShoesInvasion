from operator import length_hint
from django.db import models

# Create your models here.
class users(models.Model):
    user_id = models.IntegerField(default=0, primary_key=True)

class Shopping_Cart(models.Model):
    shopping_id = models.IntegerField(default=0, primary_key=True)
    user_id = models.ForeignKey(users, on_delete = models.CASCADE)
    product_id = models.IntegerField(default=0)
    quantity = models.IntegerField(default=0)
    size = models.CharField(max_length=5)
    color = models.CharField(max_length=45)
