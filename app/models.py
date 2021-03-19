from django.db import models
from customers .models import Customer
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw
from users.models import User


class App(models.Model):
    name = models.CharField(max_length=200 , null = False )
    description = models.CharField(max_length=500 , null=False)
    notifications_used = models.IntegerField(default=0)
    notifications_actual_used = models.IntegerField(default=0)
    customer_id  = models.ForeignKey(Customer, related_name="customer", on_delete=models.CASCADE)
    app_qr =  models.ImageField(upload_to='app_qr/', blank=True)
    created_at = models.DateField(auto_now_add=True)
    app_image = models.ImageField(upload_to='app_image/',blank=True)
    app_logo = models.ImageField(upload_to='app_logo/',blank= True)
    app_url = models.CharField(max_length=500 , null=False)
    total_notifications_sent = models.IntegerField(default=0)

    def __str__(self):
        return self.name



class UserApp(models.Model):
    app_id = models.ForeignKey(App, related_name="app", on_delete=models.CASCADE)
    user_id  = models.ForeignKey(User,related_name="user", on_delete = models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    customer_id  = models.IntegerField(null = True )
    
    # def __str__(self):
    #     return self.id
    
    
    def save(self, *args, **kwargs):
        if not self.customer_id:
            if self.user_id:
                liscname = App.objects.get(id = self.app_id.pk)
                self.customer_id = liscname.customer_id.pk
        return super(UserApp, self).save(*args, **kwargs)

class AppPrivate(models.Model):
    name = models.CharField(max_length=200 , null = False )
    description = models.CharField(max_length=500 , null=False)
    notifications_used = models.IntegerField(default=0)
    notifications_actual_used = models.IntegerField(default=0)
    customer_id  = models.ForeignKey(Customer, related_name="customer_private_app", on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    app_image = models.ImageField(upload_to='app_image/',blank=True)
    app_logo = models.ImageField(upload_to='app_logo/',blank= True)
    app_url = models.CharField(max_length=500 , null=False)



class PrivateQr(models.Model):
    app_id  = models.ForeignKey(App, related_name="private_app", on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    app_qr =  models.ImageField(upload_to='app_qr/', blank=True)
    customer_hash_code = models.CharField(max_length=500 , null=False)
    qr_used = models.BooleanField(default=False)


class PrivateUserApp(models.Model):
    Private_qr_id = models.ForeignKey(PrivateQr, related_name="private_qr", on_delete=models.CASCADE)
    user_id  = models.ForeignKey(User,related_name="private_user", on_delete = models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    customer_id  = models.IntegerField(null = True )