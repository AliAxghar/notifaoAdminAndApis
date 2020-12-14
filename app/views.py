# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template
from customers.models import Customer
from app.forms import *
from invoices.models import *
import time
import json
from app.models import *
from django.shortcuts import render
from rest_framework import viewsets
from .models import App ,UserApp
from .serializers import AppSerializer ,UserAppSerializer
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw
from django.core import serializers
from rest_framework .decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import authenticate
from customers.models import Customer
from rest_framework import status
from django.contrib.auth.decorators import login_required
from core.settings import api_base_url
import requests
from notifications.models import Notification
import stripe
stripe.api_key = "sk_test_UvbSbh6FV9UkIul1duI3oQDT00H3n6HQG0" 

@login_required(login_url="/login/")
def index(request):
    user = request.user
    customer = user.id
    apps = App.objects.filter(customer_id=customer)
    total_noti_graph_list = []
    if apps:
        for app in apps:
            total_noti_graph_data = Notification.objects.filter(app_id=app.id).order_by('-id')[:12]
            for total_noti in total_noti_graph_data:
                total_noti_graph_list.append([str(total_noti.created_at),int(total_noti.notification_count)])
    if not total_noti_graph_list:        
        total_noti_graph_list = [[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]]
    notifications = []
    a_notifications = Notification.objects.all().order_by('-id')[:7]
    if apps:
        for app in apps:
            all_notifications = Notification.objects.filter(app_id=app.id).order_by('-id')[:5]
            for noti in all_notifications:
                notifications.append(noti)
    total_users =  UserApp.objects.filter(customer_id=customer).values('user_id').distinct().count()
    lasUsers = UserApp.objects.filter(customer_id=customer).distinct('user_id')
    userapps = UserApp.objects.filter(customer_id=customer).order_by('-id')[:12]
    data = []
    labels = []
    # users_graph_data = []
    if userapps:
        for obj in userapps:
            data.append(obj.user_id.id)
            userapp_dates = str(obj.created_at)
            labels.append(userapp_dates)
    lists = []
    if userapps:
        for p in userapps:
            lists.append([str(p.created_at),int(p.user_id.id)])
    if not lists:        
        lists = [[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]]
    user_obj = Customer.objects.get(email=user.email)
    total_notification = user_obj.push_notifications
    notifications_used = user_obj.used_notifications
    if total_notification != 0:
        total_used_percent = notifications_used * 100/total_notification
        total_used_notification = round(total_used_percent)
        remaining_notification = 100 - total_used_notification
    else:
        total_used_notification = "99"
        remaining_notification = "0"
    
    if request.method == 'POST':
        dates  = request.POST.get('dates')
        lasUsers = UserApp.objects.filter(created_at=dates).order_by('-id')[:10]
        total_users =  UserApp.objects.filter(created_at=dates, customer_id=customer).values('user_id').distinct().count()
        
    context = {"total_noti_graph_list":total_noti_graph_list, "a_notifications":a_notifications, "lists":json.dumps(lists), "notifications":notifications, "lasUsers":lasUsers, "total_used_notification":total_used_notification,"remaining_notification":remaining_notification, "userapps":userapps, "total_users":total_users,"data":data, "labels":labels}
    context['segment'] = 'index'

    html_template = loader.get_template( 'index.html' )
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def pages(request):
    user = request.user
    all_app = App.objects.all()
    lasUsers = UserApp.objects.all()
    a_notifications = Notification.objects.all()
    apps = App.objects.filter(customer_id=user.id)
    notifications = []
    for app in apps:
        all_notifications = Notification.objects.filter(app_id=app.id)
        for noti in all_notifications:
            notifications.append(noti)
    Users = UserApp.objects.filter(customer_id=user.id)
    userApps = App.objects.filter(customer_id_id=user.id)
    user_obj = Customer.objects.get(email=user.email)
    total_notification = user_obj.push_notifications
    notifications_used = user_obj.used_notifications
    if total_notification != 0:
        total_used_percent = notifications_used * 100/total_notification
        total_used_notification = round(total_used_percent)
        remaining_notification = 100 - total_used_notification
    else:
        total_used_notification = "99"
        remaining_notification = "0"



    context = {"a_notifications":a_notifications, "notifications":notifications, "lasUsers":lasUsers, "all_app":all_app,"userApps":userApps,"total_used_notification":total_used_notification,"remaining_notification":remaining_notification,}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:
        
        load_template      = request.path.split('/')[-1]
        context['segment'] = load_template
        
        html_template = loader.get_template( load_template )
        return HttpResponse(html_template.render(context, request))
        
    except template.TemplateDoesNotExist:

        html_template = loader.get_template( 'page-404.html' )
        return HttpResponse(html_template.render(context, request))

    except:
    
        html_template = loader.get_template( 'page-500.html' )
        return HttpResponse(html_template.render(context, request))


class UserAppViewSet(viewsets.ModelViewSet):
    queryset = UserApp.objects.all()
    serializer_class = UserAppSerializer



class AppViewSet(viewsets.ModelViewSet):
    
    queryset = App.objects.all()
    serializer_class = AppSerializer


    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        qr_image = qrcode.make(response.data['id'])
        canvas = Image.new('RGB',(290,290), 'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qr_image)
        fname = f'app_qr-{self.name}.png'
        buffer = BytesIO()
        canvas.save(buffer,'PNG')
        obj = App.objects.get(id = response.data['id'] )
        obj.app_qr.save(fname,File(buffer),save = True)
        canvas.close()
        # super().save(*args, **kwargs)
        serializer = self.get_serializer(obj)
        return Response(serializer.data)



@api_view(['GET', 'POST'])
def createApp(request):
    if request.method == 'POST':
        user_email  = request.data['email']
        user_password = request.data['password']
        app_name = request.data['app_name']
        app_description = request.data['app_discription']
        image_app = request.data['app_image']
        app_logo  = request.POST.get('app_logo')
        
        try:
            get_custmer = Customer.objects.get(email = user_email)
        except Customer.DoesNotExist:
            get_custmer = None
        if get_custmer is None:
            return Response({"message": "Customer does not exists " , "status": status.HTTP_404_NOT_FOUND})
        else:
            pass_res = get_custmer.check_password(user_password)
            if pass_res:
                if get_custmer.apps_allowed >= 1:
                    app_obj = App.objects.create(name =app_name, description  = app_description ,app_image  = image_app , customer_id = get_custmer, app_logo=app_logo)
                    allowed_app = get_custmer.apps_allowed
                    get_custmer.apps_allowed = allowed_app - 1
                    get_custmer.save() 
                    qr_image = qrcode.make(app_obj.id)
                    canvas = Image.new('RGB',(290,290), 'white')
                    draw = ImageDraw.Draw(canvas)
                    canvas.paste(qr_image)
                    fname = f'app_qr-{app_obj.name}.png'
                    buffer = BytesIO()
                    canvas.save(buffer,'PNG')
                    obj = App.objects.get(id = app_obj.id )
                    obj.app_qr.save(fname,File(buffer),save = True)
                    app_obj2 = App.objects.get(id = app_obj.id)
                    app_obj = app_obj2
                    canvas.close()
                    return Response({
                        "id": app_obj.id,
                        "name": app_obj.name,
                        "description": app_obj.description,
                        "notifications_used": app_obj.notifications_used,
                        "app_qr": app_obj.app_qr.url ,
                        "created_at": app_obj.created_at,
                        "app_image": app_obj.app_image.url ,
                        "status": status.HTTP_200_OK,
                    })
                else:
                    return Response({"detail": "Limit reached for allowed Apps",  "status": status.HTTP_429_TOO_MANY_REQUESTS})
            else:
                return Response({"detail": "Wrong Password!",  "status": status.HTTP_401_UNAUTHORIZED})

    else:
        return Response({"detail": "Invalid Request!",  "status": status.HTTP_400_BAD_REQUEST})


@login_required(login_url="/login/")
def singleNotification(request, pk):
    notifications = Notification.objects.filter(id=pk)
    context = {"notifications":notifications,}
    return render(request, 'single-notification.html', context)

@login_required(login_url="/login/")
def deleteNotification(request, pk):
    notification = Notification.objects.get(id=pk)
    if request.method == "POST":
        notification_d = Notification.objects.filter(id=pk)
        notification_d.delete()
        return redirect("../../notification.html")
    context = {'notification': notification}
    return render(request, 'delete-notification.html', context)

@login_required(login_url="/login/")
def createPlan(request):
    user_email = request.user.email
    if request.method == "POST":
        name = request.POST.get('name')
        price = request.POST.get('price')
        interval = request.POST.get('interval')
        notifications = request.POST.get('notification')
        apps = request.POST.get('apps')
        description = request.POST.get('description')
        user = Invoices.objects.create(name=name, price=price, email=user_email, interval=interval, notifications=notifications, apps=apps, description=description)
        if user:
            return redirect("/updatePlan/")
    context = {}
    return render(request, 'my-plan.html', context)

@login_required(login_url="/login/")
def updatePlan(request):
    user_email = request.user.email
    if request.method == "POST":
        cardnumber = request.POST.get('cardnumber')
        exp_date = request.POST.get('exp-date')
        stripeToken = request.POST.get('stripeToken')
        cvc = request.POST.get('cvc')
        print(stripeToken)
        # return redirect("../../my-plan.html")
    context = {}
    return render(request, 'payment.html', context)


@login_required(login_url="/login/")
def updateProfile(request, pk):
    notifications_used = 0
    user = request.user
    user_obj = Customer.objects.get(email=user.email)
    total_notification = user_obj.push_notifications
    notifications_used = user_obj.used_notifications
    if total_notification != 0:
        total_used_percent = notifications_used * 100/total_notification
        total_used_notification = round(total_used_percent)
        remaining_notification = 100 - total_used_notification
    else:
        total_used_notification = "99"
        remaining_notification = "0"
    msg = ""
    user = Customer.objects.get(id=pk)
    form = UpdateProfileForm(request.POST or None, request.FILES or None,instance=user)
    if request.method == 'POST':
        form = UpdateProfileForm(request.POST or None, request.FILES or None, instance=user)
        if form.is_valid():
            user = form.save()
            password = form.cleaned_data.get('New_password')
            if password:
                user.set_password(password)
            user.save()
            # msg = "Profile updated successfully" 
            return redirect("/update_profile/{}/".format(user.id))										
    
    context = {'form': form, "msg":msg, "total_used_notification":total_used_notification, "remaining_notification":remaining_notification}
    return render(request, 'profile.html', context)

@login_required(login_url="/login/")
def create_apps(request):
    user = request.user
    customer_id = user.id
    user_obj = Customer.objects.get(email=user.email)
    total_notification = user_obj.push_notifications
    notifications_used = user_obj.used_notifications
    if total_notification != 0:
        total_used_percent = notifications_used * 100/total_notification
        total_used_notification = round(total_used_percent)
        remaining_notification = 100 - total_used_notification
    else:
        total_used_notification = "99"
        remaining_notification = "0"
    success = False
    if request.method == 'POST':
        form = AddAppForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            app_name = form.cleaned_data.get('name')
            app_url = form.cleaned_data.get('app_url')
            description = form.cleaned_data.get('description')
            app_logo = form.cleaned_data.get('app_logo')
            app_image = form.cleaned_data.get('app_image')
            app_obj = App.objects.create(name =app_name, description  = description ,app_image  = app_image,app_url  = app_url , customer_id_id = customer_id, app_logo=app_logo)
            allowed_app = get_custmer.apps_allowed
            get_custmer.apps_allowed = allowed_app - 1
            get_custmer.save() 
            qr_image = qrcode.make(app_obj.id)
            canvas = Image.new('RGB',(290,290), 'white')
            draw = ImageDraw.Draw(canvas)
            canvas.paste(qr_image)
            fname = f'app_qr-{app_obj.name}.png'
            buffer = BytesIO()
            canvas.save(buffer,'PNG')
            obj = App.objects.get(id = app_obj.id )
            obj.app_qr.save(fname,File(buffer),save = True)
            app_obj2 = App.objects.get(id = app_obj.id)
            app_obj = app_obj2
            canvas.close()
            if app_obj:
                success = True
                if success:
                    return redirect("../../app.html")
    else:
        form = AddAppForm(request.POST or None, request.FILES or None)
    context = {"form":form,"customer_id":customer_id, "total_used_notification":total_used_notification, "remaining_notification":remaining_notification}
    return render(request, 'add-app.html', context)

@login_required(login_url="/login/")
def updateApp(request, pk):
    user = request.user
    customer_id = user.id
    user_obj = Customer.objects.get(email=user.email)
    total_notification = user_obj.push_notifications
    notifications_used = user_obj.used_notifications
    if total_notification != 0:
        total_used_percent = notifications_used * 100/total_notification
        total_used_notification = round(total_used_percent)
        remaining_notification = 100 - total_used_notification
    else:
        total_used_notification = "99"
        remaining_notification = "0"
    msg = ""
    app = App.objects.get(id=pk)
    form = UpdateAppForm(request.POST or None, request.FILES or None,instance=app)
    if request.method == 'POST':
        form = UpdateAppForm(request.POST or None, request.FILES or None, instance=app)
        if form.is_valid():
            user = form.save()
            user.save()
            msg = "App updated successfully"
            return redirect("../../app.html")								
    
    context = {'form': form, "msg":msg,"app":app, "total_used_notification":total_used_notification, "remaining_notification":remaining_notification}
    return render(request, 'edit-app.html', context)

@login_required(login_url="/login/")
def deleteApp(request, pk):
    app = App.objects.get(id=pk)
    if request.method == "POST":
        app = App.objects.filter(id=pk)
        app.delete()
        return redirect("../../app.html")
    context = {'app': app}
    return render(request, 'delete-app.html', context)



@login_required(login_url="/login/")
def view_apps(request,pk):
    app_detail = App.objects.get(id=pk)
    context = {"app_detail":app_detail}
    return render(request, 'view-app.html', context)
