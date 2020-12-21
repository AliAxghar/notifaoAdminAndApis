from django.db import models

class Invoices(models.Model):
    billing_id = models.CharField(max_length=255,null=True,blank=True)
    name = models.CharField(max_length=255,null=True,blank=True)
    price = models.IntegerField(null= True,blank=True)
    interval = models.CharField(max_length= 255,null=True)
    notifications = models.IntegerField(null= True,blank=True)
    apps = models.IntegerField(null= True,blank=True)
    description = models.CharField (max_length=555,null= True,blank=True)
    email = models.CharField(max_length=255,null= True,blank=True)
    status  = models.CharField(max_length=255,null= True,blank=True)
    payment_method = models.CharField(max_length=255,null= True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    charge_id = models.CharField(max_length=255,null= True,blank=True)
    customer_id = models.CharField(max_length=255,null= True,blank=True)
    subscription_id = models.CharField(max_length=255,null= True,blank=True)
    subscription_created_at = models.CharField(max_length=255,null= True,blank=True)
    charge_receipt_url = models.CharField(max_length=555,null= True,blank=True)
    def __str__(self):
        return self.email

