from rest_framework import serializers
from .models import App ,UserApp


class AppSerializer(serializers.ModelSerializer):
    class Meta:
        model = App
        fields = ['id', 'name', 'description', 'notifications_used', 'customer_id', 'app_qr','created_at', 'app_image']


class UserAppSerializer (serializers.ModelSerializer):
    class Meta:
        model = UserApp
        fields = ['id','app_id','user_id','created_at']
