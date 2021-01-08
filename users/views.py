from django.shortcuts import render
from rest_framework import viewsets
from .models import User
from .serializers import UserSerializer
from rest_framework .decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework import status
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer



@api_view(['GET', 'POST'])
def customUserRegister(request):
    if request.method == 'POST':
        user_email  = request.data['email']
        user_password = request.data['password']
        user_name = request.data['name']
        user_phone = request.data['phone']
        profile_pic = request.data['profile_pic']
        try:
            get_custmer = Customer.objects.get(email = user_email)
        except Customer.DoesNotExist:
            get_custmer = None
        if get_custmer is None:
            try:
                get_custmer = Customer.objects.get(phone = user_phone)
            except Customer.DoesNotExist:
                get_custmer = None
                if get_custmer is None:
                    app_obj = User.objects.create(name =user_name, email = user_email ,profile_pic  = profile_pic , password = user_password, phone = user_phone)
                    app_obj.save()
                    if app_obj is not None:
                        return Response({"message": "Successfully created" , "status": status.HTTP_201_CREATED})
                    else:
                        return Response({"message": "User not created" , "status": status.HTTP_406_NOT_ACCEPTABLE})
                else:
                    return Response({"message": "Phone number already exists " , "status": status.HTTP_306_RESERVED})
        else:
            return Response({"message": "Email already exists " , "status": status.HTTP_306_RESERVED})
    else:
        return Response({"detail": "Invalid Request!",  "status": status.HTTP_400_BAD_REQUEST})
    


@api_view(['POST'])
def custom_user_login(request):
    if request.method == 'POST':
        user_email  = request.data['email']
        user_password = request.data['password']
       
        try:
            get_custmer = User.objects.get(email = user_email)
        except User.DoesNotExist:
            get_custmer = None
        if get_custmer is None:
            return Response({"detail": "user does not exist",  "status": status.HTTP_404_NOT_FOUND})
        else:
            if get_custmer.password == user_password:
                return Response({
                    "id": get_custmer.id,
                    "name": get_custmer.name,
                    "email": get_custmer.email,
                    "phone": get_custmer.phone,
                    "profile_pic": get_custmer.profile_pic ,
                })
            else:
                return Response({"detail": "Invalid password",  "status": status.HTTP_401_UNAUTHORIZED})
                        
    else:
        return Response({"detail": "Invalid Request!",  "status": status.HTTP_400_BAD_REQUEST})
    
