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
import requests

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