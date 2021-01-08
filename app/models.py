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
    customer_id  = models.IntegerField(null = True )
    
    # def __str__(self):
    #     return self.id
    
    
    def save(self, *args, **kwargs):
        if not self.customer_id:
            if self.user_id:
                liscname = App.objects.get(id = self.app_id.pk)
                self.customer_id = liscname.customer_id.pk
        return super(UserApp, self).save(*args, **kwargs)
