
from customers.models import Customer
from django import forms


class UpdateProfileForm(forms.ModelForm):
    New_password = forms.CharField(required=False, widget=forms.PasswordInput)
    class Meta:
        model = Customer
        fields = ('name','email','profile_pic')
        labels = {
            'name': 'Name',
            'email': 'Email', 
            'New_password':'New Password',
            'profile_pic': 'Profile picture',
        }
    def __init__(self, *args, **kwargs):
        super(UpdateProfileForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'