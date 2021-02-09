# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from customers.models import Customer

class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder" : "Email",                
                "class": "form-control"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder" : "Password",                
                "class": "form-control"
            }
        ))



class ResetPassForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder" : "Email",                
                "class": "form-control"
            }
        ))

class SignUpForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder" : "Username",                
                "class": "form-control"
            }
        ))
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder" : "Email",                
                "class": "form-control"
            }
        ))
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder" : "Password",                
                "class": "form-control"
            }
        ))
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder" : "Confirm password",                
                "class": "form-control"
            }
        ))

    class Meta:
        model = Customer
        fields = ('username', 'email', 'password1', 'password2')


# class UpdatePasswordForm(UserCreationForm):
#     password1 = forms.CharField(
#         widget=forms.PasswordInput(
#             attrs={
#                 "placeholder" : "Password",                
#                 "class": "form-control"
#             }
#         ))
#     password2 = forms.CharField(
#         widget=forms.PasswordInput(
#             attrs={
#                 "placeholder" : "Confirm password",                
#                 "class": "form-control"
#             }
#         ))

#     class Meta:
#         model = Customer
#         fields = ('password1', 'password2')

class UpdatePasswordForm(forms.ModelForm):
    password1 = forms.CharField(required=False, widget=forms.PasswordInput)
    password2 = forms.CharField(required=False, widget=forms.PasswordInput)
    class Meta:
        model = Customer
        fields = ()
        labels = {
        }
    def __init__(self, *args, **kwargs):
        super(UpdatePasswordForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs['placeholder'] = 'New password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm password'
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
