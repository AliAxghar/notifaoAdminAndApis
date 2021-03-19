from rest_framework import serializers
from .models import App ,UserApp, AppPrivate,PrivateQr,PrivateUserApp


class AppSerializer(serializers.ModelSerializer):
    class Meta:
        model = App
        fields = ['id', 'name', 'description', 'notifications_used','notifications_actual_used', 'customer_id', 'app_qr','created_at', 'app_image','app_logo']


class UserAppSerializer (serializers.ModelSerializer):

    customer_id = serializers.IntegerField(required=False)

    class Meta:
        model = UserApp
        fields = ['id','app_id','user_id','created_at','customer_id']

        def create(self, validated_data):
            return UserApp.objects.create(**validated_data)



class AppPrivateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppPrivate
        fields = ['id', 'name', 'description', 'notifications_used','notifications_actual_used', 'customer_id','created_at', 'app_image','app_logo']



class PrivateQrSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrivateQr
        fields = ['id', 'app_id', 'created_at','app_qr','customer_hash_code','qr_used']




class PrivateUserAppSerializer (serializers.ModelSerializer):

    customer_id = serializers.IntegerField(required=False)
    class Meta:
        model = PrivateUserApp
        fields = ['id','Private_qr_id','user_id','created_at','customer_id']

        def create(self, validated_data):
            return PrivateUserApp.objects.create(**validated_data)