from rest_framework import serializers
from rest_auth.models import TokenModel
from django.contrib.auth.models import User
from .models import Customer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from allauth.account.adapter import get_adapter
from rest_framework.validators import UniqueValidator
from rest_auth.registration.serializers import RegisterSerializer
from django.contrib.auth import get_user_model, authenticate

UserModel = get_user_model()

class CustomerSerializer(serializers.ModelSerializer):
    subDate = serializers.DateField(required=False)
    push_notifications = serializers.IntegerField(required=False)
    push_notifications = serializers.IntegerField(required=False)
    email_notifications = serializers.IntegerField(required=False)
    subscription_id = serializers.CharField(required=False)
    business_name = serializers.CharField(required=True)

    phone = serializers.CharField(
        max_length=100,
        validators=[UniqueValidator(queryset=Customer.objects.all())],
        required=False
    )
    email = serializers.EmailField(
        max_length=100,
        validators=[UniqueValidator(queryset=Customer.objects.all())],
        required=False
    )

    class Meta:
        model = Customer
        fields = ['id', 'name', 'email', 'phone', 'password','business_name','subDate', 'push_notifications', 'email_notifications','subscription_id','apps_allowed','profile_pic']


class MyRegisterSerializer(RegisterSerializer):
    name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    business_name = serializers.CharField(required=True)
    username = serializers.CharField(required=False)
    subDate = serializers.DateField(required=False)
    push_notifications = serializers.IntegerField(required=False)
    push_notifications = serializers.IntegerField(required=False)
    email_notifications = serializers.IntegerField(required=False)
    subscription_id = serializers.CharField(required=False)
    profile_pic = serializers.ImageField(required=False)
    # phone = serializers.CharField(required=True)
    phone = serializers.CharField(
        max_length=100,
        validators=[UniqueValidator(queryset=Customer.objects.all())]
    )

    # def validate(self, data):
    #     return data
    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError({"password": "The two password fields didn't match."})
        return data

    def get_cleaned_data(self):
        data_dict = super().get_cleaned_data()
        data_dict['name'] = self.validated_data.get('name', '')
        data_dict['email'] = self.validated_data.get('email', '')
        data_dict['phone'] = self.validated_data.get('phone', '')
        data_dict['business_name'] = self.validated_data.get('business_name', '')
        return data_dict

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)

        user.name = self.cleaned_data.get('name')
        user.email = self.cleaned_data.get('email')
        user.phone = self.cleaned_data.get('phone')
        user.business_name = self.cleaned_data.get('business_name')

        # if self.cleaned_data.get('weight') :
        #     user.weight = self.cleaned_data.get('weight')
        # # user.weight = self.cleaned_data.get('weight')
        # if self.cleaned_data.get('dob') :
        #     user.dob = self.cleaned_data.get('dob')
        user.save()
        return user

class CustomerTokenSerializer(serializers.ModelSerializer):
    user = CustomerSerializer(read_only=True)
   
    class Meta:
        model = TokenModel
        fields = ['key', 'user']



class MyLoginSerializer(serializers.Serializer):
    # username = serializers.CharField(required=False, allow_blank=True)
    email = serializers.EmailField(required=True, allow_blank=False)
    password = serializers.CharField(style={'input_type': 'password'})
    
    # def _validate_username(self, username, password):
    #     user = None

    #     if username and password:
    #         user = authenticate(username=username, password=password)
    #     else:
    #         msg = _('Must include "username" and "password".')
    #         raise exceptions.ValidationError(msg)

    #     return user

    def _validate_email(self, email, password):
        user = None

        if email and password:
            user = authenticate(email=email, password=password)
        else:
            msg = _('Must include "email" and "password".')
            raise exceptions.ValidationError(msg)

        return user

    def validate(self, attrs):
        # username = attrs.get('username')
        email = attrs.get('email')
        password = attrs.get('password')

        user = None
        
        if 'allauth' in settings.INSTALLED_APPS:
            # Authentication through email
            if app_settings.AUTHENTICATION_METHOD == app_settings.AuthenticationMethod.EMAIL:
                user = self._validate_email(email, password)

            # Authentication through username
            elif app_settings.AUTHENTICATION_METHOD == app_settings.AuthenticationMethod.USERNAME:
                user = self._validate_username(username, password)

            # Authentication through either username or email
            else:
                user = self._validate_username_email(username, email, password)

        else:
            # Authentication without using allauth
            if email:
                try:
                    username = UserModel.objects.get(email__iexact=email).get_username()
                except UserModel.DoesNotExist:
                    pass

            if username:
                user = self._validate_username_email(username, '', password)

        # Did we get back an active user?
        if user:
            if not user.is_active:
                msg = _('User account is disabled.')
                raise exceptions.ValidationError(msg)
        else:
            msg = {"message": "Unable to log in with provided credentials."}
            raise serializers.ValidationError(msg)


        attrs['user'] = user
        return attrs
