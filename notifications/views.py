from django.shortcuts import render
from customers .models import Customer
from .serializers import NotificationSerializer
from rest_framework import viewsets
from rest_framework.decorators import api_view
from app . models import App,UserApp
from rest_framework.response import Response
from rest_framework import status
from notifications .models import Notification, UserNotification
from .models import CustomFCMDevice
from users .models import User
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
import json
from notifications.serializers import DeviceSerializer ,UserNotificationSerializer


class UserNotificationViewSet(viewsets.ModelViewSet):
    queryset = UserNotification.objects.all()
    serializer_class = UserNotificationSerializer



class DeviceViewSet(viewsets.ModelViewSet):
    queryset = CustomFCMDevice.objects.all()
    serializer_class = DeviceSerializer


class NotificationViewSet(viewsets.ModelViewSet):
    
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer



@api_view(['POST'])
def getUserNotifications(request):
    if request.method == 'POST':
        try:
            user_id  = request.data['user_id']
        except MultiValueDictKeyError:
            return Response({"detail": "Make sure user_id is provided",  "status": status.HTTP_400_BAD_REQUEST})        
        try:
            get_user = User.objects.get(id = user_id)
        except User.DoesNotExist:
            get_user = None
        if get_user is not None:
            # user_app_list = UserApp.objects.filter(user_id = user_id).all()
            # for app in user_app_list:
            #     apps.
            user_apps = App.objects.filter(app__in = UserApp.objects.filter(user_id = user_id))
            user_notification = UserNotification.objects.filter(user_id = user_id)[:20]
            serializer = UserNotificationSerializer(user_notification, many=True)
            return JsonResponse(serializer.data, safe=False)
        else:
            return Response({"message": "User does not exixts " , "status": status.HTTP_400_BAD_REQUEST})
    else:
        return Response({"detail": "Invalid Request!",  "status": status.HTTP_400_BAD_REQUEST})    


@api_view(['POST'])
def createNotification(request):
    sent_count = 0
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
                try:
                    get_app = App.objects.get( name = app_name , customer_id = get_custmer.pk)
                except App.DoesNotExist:
                    get_app = None
                if get_app is not None:
                    notification_obj = Notification.objects.create(title =notification_title, description  = notification_description , app_id = get_app)
                    notification_obj.save()
                    sent_count = UserApp.objects.filter(app_id = get_app.pk).count()
                    app_users = UserApp.objects.filter(app_id = get_app.pk)
                    if get_custmer.push_notifications >= sent_count:
                        if app_users :
                            for user in app_users:
                                user_notification_obj = UserNotification.objects.create(user_id = user.user_id,title = notification_title,description = notification_description)
                                user_notification_obj.save()
                                device = CustomFCMDevice.objects.get(user_id = user.user_id)
                                device.send_message(title=notification_title, body=notification_description)
                            get_custmer.push_notifications = get_custmer.push_notifications - sent_count
                            get_custmer.save()
                            notification_obj.notification_count = sent_count
                            notification_obj.save()
                            get_app.notifications_used = get_app.notifications_used + sent_count
                            get_app.save()
                            return Response({
                                "title": notification_obj.title,
                                "description": notification_obj.description,
                                "notifications_used": notification_obj.notification_count,
                                "created_at": notification_obj.created_at,
                                "message": "success",
                                "status": status.HTTP_200_OK ,
                                })
                    else:
                        return Response({"message": "You do not have enough notifications left" , "status": status.HTTP_404_NOT_FOUND})
                else:
                    return Response({"detail": "you do not have an app with this name",  "status": status.HTTP_429_TOO_MANY_REQUESTS})
            else:
                return Response({"detail": "Wrong Password!",  "status": status.HTTP_401_UNAUTHORIZED})

    else:
        return Response({"detail": "Invalid Request!",  "status": status.HTTP_400_BAD_REQUEST})



@login_required(login_url="/login/")
def createNotificationDashboard(request):
    cUser = request.user
    user_id = cUser.id
    get_custmer = cUser
    all_apps = App.objects.filter(customer_id=user_id)
    if request.method == "POST":
        app_name = request.POST.get('app_name')
        notification_title = request.POST.get('title')
        notification_description = request.POST.get('description')
        get_app = App.objects.get( name = app_name , customer_id = user_id)
        notification_obj = Notification.objects.create(title =notification_title, description  = notification_description , app_id = get_app)
        notification_obj.save()
        sent_count = UserApp.objects.filter(app_id = get_app.pk).count()
        app_users = UserApp.objects.filter(app_id = get_app.pk)
        if get_custmer.push_notifications >= sent_count:
            if app_users :
                for user in app_users:
                    user_notification_obj = UserNotification.objects.create(user_id = user.user_id,title = notification_title,description = notification_description)
                    user_notification_obj.save()
                    device = CustomFCMDevice.objects.get(user_id = user.user_id)
                    device.send_message(title=notification_title, body=notification_description)
                get_custmer.push_notifications = get_custmer.push_notifications - sent_count
                get_custmer.save()
                notification_obj.notification_count = sent_count
                notification_obj.save()
                get_app.notifications_used = get_app.notifications_used + sent_count
                get_app.save()

        return redirect("../../notification.html")
    context = {"all_apps":all_apps}
    return render(request, 'add-notification.html', context)

@login_required(login_url="/login/")
def deleteNotification(request, pk):
    notification = Notification.objects.get(id=pk)
    if request.method == "POST":
        notification_d = Notification.objects.filter(id=pk)
        notification_d.delete()
        return redirect("../../notification.html")
    context = {'notification': notification}
    return render(request, 'delete-notification.html', context)