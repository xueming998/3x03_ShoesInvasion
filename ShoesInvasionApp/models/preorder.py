from django.db import models
from .products import ProductsTable
from .user import UserTable

class PreOrderTable(models.Model):
    product = models.ForeignKey(ProductsTable, on_delete=models.CASCADE)
    unique_id = models.ForeignKey(UserTable, to_field="unique_id", db_column="unique_id", on_delete=models.CASCADE)

    def __str__(self):
        return self.product