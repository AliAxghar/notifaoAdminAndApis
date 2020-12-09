from django.db import models

class User (models.Model):
    name = models.CharField(max_length= 50,null= False)
    email = models.EmailField(null=False,unique=True)
    password = models.CharField(max_length=100,null=False)
    phone = models.CharField(max_length=100,null=False,unique=True)
    profile_pic = models.ImageField(upload_to='user_image/',blank= True)

    def __str__(self):
        return self.name