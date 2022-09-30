from django.db import models
from datetime import date
from .user import UserTable

class TransactionTable(models.Model):
    createdDate = models.DateField(default=date.today)
    user = models.ForeignKey(UserTable, to_field="unique_id", db_column="unique_id", on_delete=models.CASCADE, unique=True)

    def __str__(self):
        return self.transaction_id