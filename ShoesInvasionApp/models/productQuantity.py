from django.db import models
from .products import ProductsTable

class ProductQuantityTable(models.Model):
    product = models.ForeignKey(ProductsTable, on_delete=models.CASCADE)
    size = models.CharField(max_length=5)
    quantity = models.IntegerField(default=0)
    color = models.CharField(max_length=45)

    def __str__(self):
        return self.product