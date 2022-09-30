from unittest.util import _MAX_LENGTH
from django.db import models
from datetime import date
from .user import UserTable

class UserDetailsTable(models.Model):
    MALE = 'M'
    FEMALE = 'F'
    GENDER_CHOICES = [
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    ]
    
    address = models.CharField(max_length=150)
    email = models.EmailField(max_length=255)
    date_of_birth = models.DateField(default=date.today)
    # gender = models.CharField(max_length=10)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default=MALE)
    phone = models.IntegerField()
    # Unique Identifier
    unique_id = models.ForeignKey(UserTable, to_field="unique_id", db_column="unique_id", on_delete=models.CASCADE, unique=True)

    def __str__(self):
        return self.username