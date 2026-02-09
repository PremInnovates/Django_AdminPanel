from django import forms
from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm


class CustomAuthAdminForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['autofocus'] = False
        self.fields['username'].widget.attrs['class'] = 'form-control input-lg'
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['password'].widget.attrs['class'] = 'form-control input-lg'
        self.fields['password'].widget.attrs['placeholder'] = 'Password'
