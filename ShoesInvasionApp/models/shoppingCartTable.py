from django.db import models
from .user import UserTable
from .products import ProductsTable

class ShoppingCartTable(models.Model):
    user = models.ForeignKey(UserTable, to_field="unique_id", db_column="unique_id", on_delete = models.CASCADE)
    product = models.ForeignKey(ProductsTable, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    size = models.CharField(max_length=10)
    color = models.CharField(max_length=45)
    total_price = models.DecimalField(default=0, decimal_places=2, max_digits=6)
    status = models.CharField(max_length=20)

    def __str__(self):
        return self.shopping_id
    
    @property
    def getCurrentProductTotal(self):
        total = self.product.product_price * self.quantity
        return total
    
    @property
    def getCartTotal(self):
        orderItems = ShoppingCartTable.objects.filter(user=self.user.unique_id)
        total = sum([item.getCurrentProductTotal for item in orderItems])
        return total
    
