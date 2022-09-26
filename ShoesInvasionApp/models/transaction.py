from django.db import models
from datetime import date
from .user import UserTable

class TransactionTable(models.Model):
    createdDate = models.DateField(default=date.today)
    user = models.ForeignKey(UserTable, on_delete=models.CASCADE)

    def __str__(self):
        return self.transaction_id