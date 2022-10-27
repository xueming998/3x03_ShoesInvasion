from django.db import models

class ProductsTable(models.Model):
    product_name = models.CharField(max_length=45)
    product_price = models.DecimalField(default=0, decimal_places=2, max_digits=6)
    review = models.TextField(default="")
    product_info = models.TextField(default="")
    product_brand = models.CharField(max_length=45)
    product_category = models.CharField(max_length=45)
    gender_type = models.CharField(max_length=10)
    available = models.CharField(max_length=3)
    status = models.CharField(max_length=60, null=True)

    def __str__(self):
        return self.product_name
