from django.db import models
from datetime import date

class UserTable(models.Model):
    MALE = 'M'
    FEMALE = 'F'
    GENDER_CHOICES = [
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    ]
    
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    address = models.CharField(max_length=150)
    email = models.EmailField(max_length=255)
    date_of_birth = models.DateField(default=date.today)
    # gender = models.CharField(max_length=10)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default=MALE)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=70)
    verify_password = models.CharField(max_length=255, null=True)
    phone = models.IntegerField()
    # True = Banned, None/Null/False = Not Banned
    bannedStatus = models.BooleanField()
    # True = Verified, None/Null/False = Not Verified
    verifiedStatus = models.BooleanField()
    # Used to store random generated verify code, empty it when account verified
    verificationCode = models.PositiveSmallIntegerField(null=True)
    # True = Locked, None/Null/False = Not Locked
    lockedStatus = models.BooleanField()
    lockedCounter = models.PositiveSmallIntegerField(null=True)
    # User = Normal User, Editor = Editor, Admin = Administrator
    accountType = models.CharField(max_length=10, default="User")

    def __str__(self):
        return self.username