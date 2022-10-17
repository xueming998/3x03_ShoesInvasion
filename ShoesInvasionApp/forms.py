from ctypes.wintypes import SIZE
from unittest.util import _MAX_LENGTH
from django import forms  
from .models.user import UserTable  
from django.contrib.auth.hashers import make_password

import bcrypt
import secrets
import string
  
class RegisterForm(forms.ModelForm):  
    class Meta:  
        model = UserTable  
        fields = '__all__'
        # exclude = ['bannedStatus', 'verifiedStatus', 'lockedStatus', 'lockedCounter', 'verificationCode', 'accountType', 'unique_id']
        widgets = {
            'password': forms.PasswordInput(),
            'verify_password': forms.PasswordInput(),
            'phone': forms.NumberInput(attrs={'min': 60000000, 'max': 99999999}),
            'bannedStatus': forms.HiddenInput(attrs={'value': 0}),
            'verifiedStatus': forms.HiddenInput(attrs={'value': 0}),
            'lockedStatus': forms.HiddenInput(attrs={'value': 0}),
            'lockedCounter': forms.HiddenInput(attrs={'value': 0}),
            'verificationCode': forms.HiddenInput(attrs={'value': 0}),
            'accountType': forms.HiddenInput(attrs={'value': 'User'}),
            'unique_id': forms.HiddenInput(attrs={'value': '123321'})
        }

    # Function used for validation
    def clean(self):
        super(RegisterForm, self).clean()

        password = self.cleaned_data.get('password')
        verifyPassword = self.cleaned_data.get('verify_password')
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        phone = self.cleaned_data.get('phone')

        if UserTable.objects.filter(username=username).exists():
            self.errors['username'] = self.error_class(['Username already taken.'])
        else:
            if UserTable.objects.filter(email=email).exists():
                self.errors['email'] = self.error_class(['Email already taken/registered.'])
            else:
                if UserTable.objects.filter(phone=phone).exists():
                    self.errors['phone'] = self.error_class(['Phone already taken/registered.'])
                else:
                    if (password != verifyPassword):
                        self.errors['verify_password'] = self.error_class(['Password does not match.'])
                    else:
                        # salt = bcrypt.gensalt()
                        # encryptedPassword = bcrypt.hashpw(password.encode('utf-8'), salt)
                        # print("Password: ", make_password(password))
                        self.cleaned_data['password'] = make_password(password)
                        self.cleaned_data['verify_password'] = make_password(password)
                        unique = ''.join(secrets.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for i in range (200))
                        self.cleaned_data['unique_id'] = unique
                        return self.cleaned_data
