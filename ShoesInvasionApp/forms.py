from ctypes.wintypes import SIZE
from dataclasses import field
from faulthandler import disable
from unittest.util import _MAX_LENGTH
from django import forms  
from .models.user import UserTable  
from django.contrib.auth.hashers import make_password
from django.forms import ModelForm
from ShoesInvasionApp.models import UserTable, UserDetailsTable  
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
import pwnedpasswords
import os

import requests, secrets, string
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox

class RegisterForm(forms.ModelForm):  
    class Meta:  
        model = UserTable  
        fields = '__all__'
        exclude = ['secret_key']
        widgets = {
            'password': forms.PasswordInput(),
            'verify_password': forms.PasswordInput(),
            'phone': forms.NumberInput(attrs={'min': 60000000, 'max': 99999999}),
            'bannedStatus': forms.HiddenInput(attrs={'value': False}),
            'verifiedStatus': forms.HiddenInput(attrs={'value': False}),
            'lockedStatus': forms.HiddenInput(attrs={'value': 0}),
            'lockedCounter': forms.HiddenInput(attrs={'value': 0}),
            'verificationCode': forms.HiddenInput(attrs={'value': 0}),
            'accountType': forms.HiddenInput(attrs={'value': 'User'}),
            'unique_id': forms.HiddenInput(attrs={'value': '123321'}),
        }

    # Function used for validation
    def clean(self):
        super(RegisterForm, self).clean()
        password = self.cleaned_data.get('password')
        verifyPassword = self.cleaned_data.get('verify_password')
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        phone = self.cleaned_data.get('phone')
        # To do a threshold check on user entering commonly used password 
        # Setting threshold to be maximum 1000 times from pwned password database
        pwnedoutput = pwnedpasswords.check(password)
        commonPasswordThreshold = 1000

        if (len(password) < 12 ):
            self.errors['password'] = self.error_class(['Password have to be at least 12 characters long.'])
        else:
            if (len(verifyPassword) < 12 ):
                self.errors['verifyPassword'] = self.error_class(['Password have to be at least 12 characters long.'])
            else:
                if (pwnedoutput > commonPasswordThreshold):
                    self.errors['password'] = self.error_class(["This is a commonly used password. Please enter another password."])
                else:
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
                                    self.cleaned_data['password'] = make_password(password)
                                    self.cleaned_data['verify_password'] = make_password(password)
                                    unique = ''.join(secrets.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for i in range (200))
                                    self.cleaned_data['unique_id'] = unique
                                    vCode = ''.join(secrets.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for i in range (20))
                                    self.cleaned_data['verificationCode'] = vCode
                                    return self.cleaned_data

class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Username'}),
        label="Username")

    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password'}))

    otpToken = forms.IntegerField(widget=forms.NumberInput(
        attrs={'class': 'form-control', 'placeholder': 'OTP Token', 'oninput': 'limit_input()', 'id': 'otpToken'}),
        label="OTP Token",
        required=False)

    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())

    def clean(self):
        super(UserLoginForm, self).clean()
        ca = self.request.POST["g-recaptcha-response"]
        url = "https://www.google.com/recaptcha/api/siteverify"
        params = {
            'secret': os.getenv('user_login_captcha_secretkey'),
            'response': ca,
        }
        verify_rs = requests.get(url, params=params, verify=True)
        verify_rs = verify_rs.json()
        status = verify_rs.get("success", False)
        if not status:
            raise forms.ValidationError(
                _('Captcha Validation Failed.'),
                code='invalid',
            )


class updateProfileForm(ModelForm):
    class Meta:
        model = UserTable
        fields = ['first_name', 'last_name', 'email', 'phone', 'username']


    def __init__(self, *args, **kwargs):
        super(updateProfileForm, self).__init__(*args, **kwargs)

    first_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter First Name'}),
        label="First Name")
    
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter Last Name'}),
        label="Last Name")
    
    email = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter Email'}),
        label="Email")
    email.disabled = True
    
    phone = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter Phone Number'}),
        label="Phone Number")
    
    def clean(self):
        super(updateProfileForm, self).clean()
