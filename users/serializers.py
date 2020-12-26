from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    profile_pic = serializers.ImageField(required=False)

    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'phone', 'profile_pic']