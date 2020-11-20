from django.db import models
from django.contrib.auth.models import AbstractUser

class Customer(AbstractUser):

    phone = models.CharField(max_length=35, null=True)
    name = models.CharField(max_length=100, null=True)
    subDate = models.DateField(auto_now_add = True)
    push_notifications = models.IntegerField(default=0)
    business_name = models.CharField(max_length=100,default= 'None')
    email_notifications = models.IntegerField(default=0)
    subscription_id = models.CharField(max_length=50,null=True)
    apps_allowed = models.IntegerField(default=0)
    used_notifications = models.IntegerField(default=0)
    profile_pic = models.ImageField(upload_to='customer_image/',blank= True)

    

    def __str__(self):
        return self.name
