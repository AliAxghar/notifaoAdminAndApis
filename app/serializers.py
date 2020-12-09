from rest_framework import serializers
from .models import App ,UserApp


class AppSerializer(serializers.ModelSerializer):
    class Meta:
        model = App
        fields = ['id', 'name', 'description', 'notifications_used', 'customer_id', 'app_qr','created_at', 'app_image','app_logo']


class UserAppSerializer (serializers.ModelSerializer):

    customer_id = serializers.IntegerField(required=False)

    class Meta:
        model = UserApp
        fields = ['id','app_id','user_id','created_at','customer_id']

        def create(self, validated_data):
            return UserApp.objects.create(**validated_data)

