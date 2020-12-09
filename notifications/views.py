from django.shortcuts import render
from customers .models import Customer
from .serializers import NotificationSerializer
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from notifications .models import Notification


class NotificationViewSet(viewsets.ModelViewSet):
    
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer


