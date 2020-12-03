from django.db import models
from customers .models import Customer
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw
from users.models import User


class App(models.Model):
    name = models.CharField(max_length=200 , null=False)
    description = models.CharField(max_length=500 , null=False)
    notifications_used = models.IntegerField(default=0)
    customer_id  = models.ForeignKey(Customer, related_name="customer", on_delete=models.CASCADE)
    app_qr =  models.ImageField(upload_to='app_qr/', blank=True)
    created_at = models.DateField(auto_now_add=True)
    app_image = models.ImageField(upload_to='app_image/',blank=True)
    app_logo = models.ImageField(upload_to='app_logo/',blank= True)
    app_url = models.CharField(max_length=500 , null=False)

    def __str__(self):
        return self.name



class UserApp(models.Model):
    app_id = models.ForeignKey(App, related_name="app", on_delete=models.CASCADE)
    user_id  = models.ForeignKey(User,related_name="user", on_delete = models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    # customer_id  = models.ForeignKey(Customer,related_name="cust_id", on_delete = models.CASCADE)
    def __str__(self):
        return self.id
