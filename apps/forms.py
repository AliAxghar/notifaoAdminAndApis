from .models import *
from django import forms


# class AppForm(forms.ModelForm):
#     class Meta:
#         model = App
#         fields = ('name','app_url','description','notifications_used','customer_id','app_qr','created_at','app_image','app_logo')
#         labels = {
#             'name': 'Name',
#             'description': 'Description', 
#             'New_password':'New Password',
#             'profile_pic': 'Profile picture',
#         }
#     def __init__(self, *args, **kwargs):
#         super(UpdateProfileForm, self).__init__(*args, **kwargs)
#         for visible in self.visible_fields():
#             visible.field.widget.attrs['class'] = 'form-control'