from unittest.util import _MAX_LENGTH
from django.db import models
from datetime import date

class UserTable(models.Model):    
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    # gender = models.CharField(max_length=10)
    username = models.CharField(max_length=255)
    password = models.BinaryField(max_length=60)
    verify_password = models.CharField(max_length=255, null=True)
    # Email
    email = models.EmailField(max_length=255)
    # Phone
    phone = models.IntegerField()
    # True = Banned, None/Null/False = Not Banned
    bannedStatus = models.BooleanField(default=False)
    # True = Verified, None/Null/False = Not Verified
    verifiedStatus = models.BooleanField()
    # Used to store random generated verify code, empty it when account verified
    verificationCode = models.PositiveSmallIntegerField(null=True)
    # True = Locked, None/Null/False = Not Locked
    lockedStatus = models.BooleanField()
    lockedCounter = models.PositiveSmallIntegerField(null=True)
    # User = Normal User, Editor = Editor, Admin = Administrator
    accountType = models.CharField(max_length=10, default="User")
    # Unique Identifier
    unique_id = models.CharField(max_length=255, unique=True, null=False, default="")

    def __str__(self):
        return self.username