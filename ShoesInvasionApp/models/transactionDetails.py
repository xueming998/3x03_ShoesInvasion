from django.db import models
from .transaction import TransactionTable
from .products import ProductsTable

class TransactionDetailsTable(models.Model):
    transaction = models.ForeignKey(TransactionTable, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductsTable, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    size = models.CharField(max_length=5)
    amount = models.DecimalField(default=0, decimal_places=2, max_digits=6)

    def __str__(self):
        return self.transaction