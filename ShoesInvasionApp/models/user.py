from django.db import models
from datetime import date

class UserTable(models.Model):
    fname = models.CharField(max_length=45)
    lname = models.CharField(max_length=45)
    address = models.TextField(default="")
    email = models.CharField(max_length=255)
    dob = models.DateField(default=date.today)
    gender = models.CharField(max_length=10)
    username = models.CharField(max_length=255)
    password = models.BinaryField(max_length=60)
    phone = models.IntegerField(default=0)
    # True = Banned, None/Null/False = Not Banned
    banned_status = models.BooleanField()
    # True = Verified, None/Null/False = Not Verified
    verifiedStatus = models.BooleanField()
    # Used to store random generated verify code, empty it when account verified
    verificationCode = models.PositiveSmallIntegerField()
    # True = Locked, None/Null/False = Not Locked
    lockedStatus = models.BooleanField()
    lockedCounter = models.PositiveSmallIntegerField()
    # User = Normal User, Editor = Editor, Admin = Administrator
    accountType = models.CharField(max_length=10, default="User")

    def __str__(self):
        return self.fname