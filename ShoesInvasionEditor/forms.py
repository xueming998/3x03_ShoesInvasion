from ctypes.wintypes import SIZE
from dataclasses import field, fields
from pyexpat import model
from secrets import choice
from unittest.util import _MAX_LENGTH
from django import forms  
from ShoesInvasionApp.models import ProductsTable  
from django.contrib.auth.hashers import make_password
from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import AuthenticationForm
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
import requests

statusChoice = (
    ('1', 'Available'),
    ('2', 'PreOrder')
)
genderChoice = (
    ('M', 'Male'), ('L', 'Female'), ('U', 'Unisex'),
)
categoryChoice = (
    ('Sneakers', 'Sneakers'), ('Formal', 'Formal'), ('Sports', 'Sports'), ('Casual', 'Casual'), ('Shoes', 'Shoes'),
)

class createProductForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(createProductForm, self).__init__(*args, **kwargs)

    product_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Puma Balanced'}),
        label="Product Name*")

    product_price = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': '$150', 'type':'number'}),
        label="Product Price*")
    
    product_info = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'Sample information about product.'}),
        label="Product Info*")

    product_brand = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'E.g. Nike, Adidas'}),
        label="Product Brand*")

    gender = forms.ChoiceField(label="Gender*", choices=genderChoice)
    status = forms.ChoiceField(label="Availability*", choices=statusChoice)
    category = forms.ChoiceField(label="Category*", choices=categoryChoice)
    
    # Function used for validation
    def clean(self):
        super(createProductForm, self).clean()
        return self.cleaned_data
    
class updateProductForm(ModelForm):
    class Meta:
        model = ProductsTable
        fields = ['product_name', 'product_price', 'product_info', 'product_brand','gender_type', 'status', 'product_category',  ]

    product_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Puma Balanced'}),
        label="Product Name*")

    product_price = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': '$150', 'type':'number'}),
        label="Product Price*")
    
    product_info = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'Sample information about product.'}),
        label="Product Info*")

    product_brand = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'E.g. Nike, Adidas'}),
        label="Product Brand*")

    gender_type = forms.ChoiceField(label="Gender*", choices=genderChoice)
    status = forms.ChoiceField(label="Availability*", choices=statusChoice)
    product_category = forms.ChoiceField(label="Category*", choices=categoryChoice)

class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Username or Email'}),
        label="Username or Email*")

    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password'}))

    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())

    def clean(self):
        super(UserLoginForm, self).clean()
        ca = self.request.POST["g-recaptcha-response"]
        url = "https://www.google.com/recaptcha/api/siteverify"
        params = {
            'secret': '6LdwPcUiAAAAAFot1LqP3dQbUbcqGNW1UR5FR36G',
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