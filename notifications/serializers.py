from rest_framework import serializers
from .models import Notification
from .models import CustomFCMDevice

class NotificationSerializer(serializers.ModelSerializer):


    created_at = serializers.DateField(required = False)
    class Meta:
        model = Notification
        fields = ['id', 'title', 'description', 'app_id', 'created_at','notification_count']



class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomFCMDevice
        fields = ['device_id','registration_id','type','name','active','user']