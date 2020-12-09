from django.db import models
from app .models import App
from io import BytesIO
from users.models import User


class Notification(models.Model):
    title = models.CharField(max_length=200 , null=False)
    description = models.CharField(max_length=500 , null=False)
    app_id  = models.ForeignKey(App, related_name="app_notification", on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    notification_count = models.IntegerField(default = 0)
    # notification_image = models.ImageField(upload_to='notification_image/',blank=True)
    # notification_logo = models.ImageField(upload_to='notification_logo/',blank= True)

    def __str__(self):
        return self.title



# class UserApp(models.Model):
#     app_id = models.ForeignKey(App, related_name="app", on_delete=models.CASCADE)
#     user_id  = models.ForeignKey(User,related_name="user", on_delete = models.CASCADE)
#     created_at = models.DateField(auto_now_add=True)
#     customer_id  = models.IntegerField(null = True )
