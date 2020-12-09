from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):


    created_at = serializers.DateField(required = False)
    class Meta:
        model = Notification
        fields = ['id', 'title', 'description', 'app_id', 'created_at']
