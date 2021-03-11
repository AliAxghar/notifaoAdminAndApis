
from customers.models import Customer
from django import forms
from app.models import App
from django.contrib.auth.forms import UserCreationForm

class UpdateProfileForm(forms.ModelForm):
    New_password = forms.CharField(required=False, widget=forms.PasswordInput)
    class Meta:
        model = Customer
        fields = ('name','email' ,'business_name', 'profile_pic')
        labels = {
            'name': 'Name',
            'email': 'Email',
            'business_name':'Business Name',
            'New_password':'New Password',
            'profile_pic': 'Profile picture',
        }
    def __init__(self, *args, **kwargs):
        super(UpdateProfileForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class AddAppForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder" : "Enter App Name", 
                "class": "form-control"
            }
        ))
    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "rows":5,
                "class": "form-control",
                "placeholder" : "Enter App Description"
                }
            ))
    app_url = forms.CharField(
        # required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder" : "Enter URL get/post", 
                "class": "form-control"
            }
        ))
    app_logo = forms.ImageField(
        widget=forms.FileInput(
            attrs={             
                "id": "fusk"
            }
        ))
    app_image = forms.ImageField(
        widget=forms.FileInput(
            attrs={             
                "id": "fusk1"
            }
        ))
    customer_id_id = forms.CharField(
        widget=forms.HiddenInput(
            attrs={
            }
        ))
    class Meta:
        model = App
        fields = ('name', 'description', 'app_logo','app_image','customer_id_id')


class UpdateAppForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder" : "Enter App Name", 
                "class": "form-control"
            }
        ))
    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "rows":5,
                "class": "form-control",
                "placeholder" : "Enter App Description"
                }
            ))
    app_url = forms.CharField(
        # required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder" : "Enter URL get/post", 
                "class": "form-control"
            }
        ))
    app_logo = forms.ImageField(
        required=False,
        widget=forms.FileInput(
            attrs={             
                "id": "fusk",
                "class": "form-control"
            }
        ))
    app_image = forms.ImageField(
        required=False,
        widget=forms.FileInput(
            attrs={             
                "id": "fusk1",
                "class": "form-control",
            }
        ))
    # customer_id_id = forms.CharField(
    #     widget=forms.HiddenInput(
    #         attrs={
    #         }
    #     ))
    class Meta:
        model = App
        fields = ('name', 'app_logo','app_image', 'app_url', 'description')

