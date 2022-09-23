from django.db import models
from .user import UserTable
from .products import ProductsTable

class ShoppingCartTable(models.Model):
    user = models.ForeignKey(UserTable, on_delete = models.CASCADE)
    product = models.ForeignKey(ProductsTable, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    size = models.CharField(max_length=10)
    color = models.CharField(max_length=45)
    total_price = models.DecimalField(default=0, decimal_places=2, max_digits=6)
    status = models.CharField(max_length=20)

    def __str__(self):
        return self.shopping_id