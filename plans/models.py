from django.db import models


class Plan (models.Model):
    name = models.CharField(max_length= 50,null= False)
    price = models.IntegerField(null= False)
    duration = models.CharField(max_length= 50,null=False)
    notifications = models.IntegerField(null=False)
    emails = models.IntegerField(null=False)
    apps = models.IntegerField(null=False)
    description = models.TextField (null=True)