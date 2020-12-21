from django.shortcuts import render
from customers .models import Customer
from .serializers import NotificationSerializer
from rest_framework import viewsets
from rest_framework.decorators import api_view
from app . models import App,UserApp
from rest_framework.response import Response
from rest_framework import status
from notifications .models import Notification
from .models import CustomFCMDevice
from notifications.serializers import DeviceSerializer


class DeviceViewSet(viewsets.ModelViewSet):
    queryset = CustomFCMDevice.objects.all()
    serializer_class = DeviceSerializer


class NotificationViewSet(viewsets.ModelViewSet):
    
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer


@api_view(['GET', 'POST'])
def createNotification(request):
    if request.method == 'POST':
        user_email  = request.data['email']
        user_password = request.data['password']
        app_name = request.data['app_name']
        notification_title = request.data['title']
        notification_description = request.data['description']
        
        try:
            get_custmer = Customer.objects.get(email = user_email)
        except Customer.DoesNotExist:
            get_custmer = None
        if get_custmer is None:
            return Response({"message": "Customer does not exists " , "status": status.HTTP_404_NOT_FOUND})
        else:
            pass_res = get_custmer.check_password(user_password)
            if pass_res:
                get_app = App.objects.get( name = app_name , customer_id = get_custmer.pk)
                if get_app:
                    notification_obj = Notification.objects.create(title =notification_title, description  = notification_description , app_id = get_app.pk)
                    return Response({
                        "title": app_obj.name,
                        "description": notification_obj.description,
                        "notifications_used": app_obj.notifications_used,
                        "created_at": notification_obj.created_at,
                        
                    })
                else:
                    return Response({"detail": "you do not have an app with this name",  "status": status.HTTP_429_TOO_MANY_REQUESTS})
            else:
                return Response({"detail": "Wrong Password!",  "status": status.HTTP_401_UNAUTHORIZED})

    else:
        return Response({"detail": "Invalid Request!",  "status": status.HTTP_400_BAD_REQUEST})

