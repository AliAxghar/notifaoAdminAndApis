from django.db import models

class Invoices(models.Model):
    billing_id = models.CharField(max_length=255,null=True)
    name = models.CharField(max_length=100,null=True)
    price = models.IntegerField(null= False)
    interval = models.CharField(max_length= 50,null=False)
    notifications = models.IntegerField(null=False)
    apps = models.IntegerField(null=False)
    description = models.TextField (null=True)
    email = models.CharField(max_length=100,null=True)
    status  = models.BooleanField(default=True)
    payment_method = models.CharField(max_length=100,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null = True)
    charge_id = models.CharField(max_length=255,null=True)
    customer_id = models.CharField(max_length=255,null=True)
    subscription_id = models.CharField(max_length=255,null=True)
    subscription_status = models.CharField(max_length=100,null=True)

    def __str__(self):
        return self.email

