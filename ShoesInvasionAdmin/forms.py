from ctypes.wintypes import SIZE
from dataclasses import field, fields
from pyexpat import model
from secrets import choice
from unittest.util import _MAX_LENGTH
from django import forms  
from django.contrib.auth.hashers import make_password
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
import requests, string, secrets

class AdminLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(AdminLoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Username or Email'}),
        label="Username")

    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password'}))

    otpToken = forms.IntegerField(widget=forms.NumberInput(
        attrs={'class': 'form-control', 'placeholder': 'OTP Token', 'oninput': 'limit_input()', 'id': 'otpToken'}),
        label="OTP Token",
        required=False)

    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())

    

    def clean(self):
        super(AdminLoginForm, self).clean()
        ca = self.request.POST["g-recaptcha-response"]
        url = "https://www.google.com/recaptcha/api/siteverify"
        params = {
            'secret': '6LeT_rciAAAAACCmGM-MTK9x5Pogedk3VUMV8c0T',
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

class RegisterEditorForm(forms.Form):  
    def __init__(self, *args, **kwargs):
        super(RegisterEditorForm, self).__init__(*args, **kwargs)

    first_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'E.g John'}),
        label="First Name")

    last_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'E.g Lim', }),
        label="Last Name")
    
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'E.g johnlim123'}),
        label="Username")

    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'E.g. ilovedogs'}),
        label="Password")

    verify_password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'E.g. Nike, Adidas'}),
        label="Verify Password")

    email = forms.CharField(widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'E.g. johnlimdogs@gmail.com'}),
        label="Email")

    phone = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'E.g. 8765 4321', 'type':'number'}),
        label="Phone Number")
    
    bannedStatus = forms.HiddenInput()
    verifiedStatus = forms.HiddenInput()
    verificationCode = forms.HiddenInput()
    lockedStatus = forms.HiddenInput()
    lockedCounter = forms.HiddenInput()
    accountType = forms.HiddenInput()
    unique_id = forms.HiddenInput()
    secret_key = forms.HiddenInput()

    # Function used for validation
    def clean(self):
        super(RegisterEditorForm, self).clean()
        return self.cleaned_data