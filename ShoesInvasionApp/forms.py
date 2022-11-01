from ctypes.wintypes import SIZE
from dataclasses import field
from faulthandler import disable
from tkinter import DISABLED
from unittest.util import _MAX_LENGTH
from django import forms  
from .models.user import UserTable  
from django.contrib.auth.hashers import make_password
from django.forms import ModelForm
from ShoesInvasionApp.models import UserTable, UserDetailsTable  
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

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
        if (len(password) < 12 ):
            self.errors['password'] = self.error_class(['Password have to be at least 12 characters long.'])
        else:
            if (len(verifyPassword) < 12 ):
                self.errors['verifyPassword'] = self.error_class(['Password have to be at least 12 characters long.'])
            else:
                if UserTable.objects.filter(username=username).exists():
                    print("verifiedStatus")
                    self.errors['username'] = self.error_class(['Username already taken.'])
                else:
                    if UserTable.objects.filter(email=email).exists():
                        self.errors['email'] = self.error_class(['Email already taken/registered.'])
                    else:
<<<<<<< HEAD
                        self.cleaned_data['password'] = make_password(password)
                        self.cleaned_data['verify_password'] = make_password(password)
                        unique = ''.join(secrets.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for i in range (200))
                        self.cleaned_data['unique_id'] = unique
                        vCode = ''.join(secrets.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for i in range (20))
                        self.cleaned_data['verificationCode'] = vCode
                        return self.cleaned_data
=======
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
                                return self.cleaned_data
>>>>>>> ab21b74e6d64eb5d862cbd95efbda1150ecf5d80

class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Username or Email'}),
        label="Username or Email*")

    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password'}))

    otpToken = forms.IntegerField(widget=forms.NumberInput(
        attrs={'class': 'form-control', 'placeholder': 'OTP Token', 'oninput': 'limit_input()', 'id': 'otpToken'}),
        label="OTP Token",
        required=False)

    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())

    def clean(self):
        super(UserLoginForm, self).clean()
        password = self.cleaned_data.get('password')
        if (len(password) < 12 ):
            self.errors['username'] = self.error_class(['Username already taken.'])
        else: pass
        ca = self.request.POST["g-recaptcha-response"]
        url = "https://www.google.com/recaptcha/api/siteverify"
        params = {
            'secret': '6Lcax7QiAAAAAPDiSYSHISAGMqiMW6E01YsrtwDQ',
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
        print("status = " + status)


class updateProfileForm(ModelForm):
    class Meta:
            # model = UserDetailsTable
            # fields = ['address', ]
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
    
    # address = forms.CharField(widget=forms.TextInput(
    #     attrs={'class': 'form-control', 'placeholder': 'Enter Address'}),
    #     label="Address")
    
    email = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter Email'}),
        label="Email")
    email.disabled = True
    
    phone = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter Phone Number'}),
        label="Phone Number")
    
    def clean(self):
        super(updateProfileForm, self).clean()