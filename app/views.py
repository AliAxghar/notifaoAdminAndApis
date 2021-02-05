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
from django.contrib.admin.models import LogEntry
from app.forms import *
from invoices.models import *
import time
import boto3
# from .forms import *
# from app.forms import UpdateAppForm
from datetime import datetime
from django.http import HttpResponse
from django.http import JsonResponse
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
from botocore.exceptions import ClientError
from core.settings import api_base_url
from core import settings
from .forms import *
import requests
# from django.conf import FCM_DJANGO_SETTINGS
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView
from notifications.models import Notification
from django.utils.datastructures import MultiValueDictKeyError
import stripe
stripe.api_key = "sk_test_UvbSbh6FV9UkIul1duI3oQDT00H3n6HQG0" 

@login_required(login_url="/login/")
def index(request):
    user = request.user
    customer = user.id
    # total_users =  UserApp.objects.filter(customer_id=customer).values('user_id').distinct().count()
    # lasUsers = UserApp.objects.all().order_by('-id')[:10]
    # userapps = UserApp.objects.all().order_by('-id')[:9]
    # data = []
    # labels = []
    # for obj in userapps:
    #     data.append(obj.user_id.id)
    #     userapp_dates = str(obj.created_at)
    #     labels.append(userapp_dates)
    apps = App.objects.filter(customer_id=customer)
    invoice_item = Invoices.objects.filter(email=user.email)
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
            all_notifications = Notification.objects.filter(app_id=app.id).order_by('-id')[:3]
            for noti in all_notifications:
                notifications.append(noti)
    total_users =  UserApp.objects.filter(customer_id=customer).values('user_id').count()
    lasUsers = UserApp.objects.filter(customer_id=customer).distinct('user_id')[:10]
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
        notifications = Notification.objects.filter(created_at=dates).order_by('-id')[:10]
        total_users =  UserApp.objects.filter(created_at=dates, customer_id=customer).values('user_id').count()
    else:
        if request.user.is_superuser:
            lasUsers = UserApp.objects.filter().distinct('user_id')
    context = {"invoice_item":invoice_item, "total_noti_graph_list":total_noti_graph_list, "a_notifications":a_notifications, "lists":json.dumps(lists), "notifications":notifications, "lasUsers":lasUsers, "total_used_notification":total_used_notification,"remaining_notification":remaining_notification, "userapps":userapps, "total_users":total_users,"data":data, "labels":labels}
    context['segment'] = 'index'

    html_template = loader.get_template( 'index.html' )
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    user = request.user
    all_app = App.objects.all()
    invoice_item = Invoices.objects.filter(email=user.email)
    # all_invoices = stripe.Invoice.list()
    total_users =  UserApp.objects.filter(customer_id=user.id).values('user_id').count()
    all_invoices = []
    invoices_a = Invoices.objects.all()
    if invoices_a:
        for i in invoices_a:
            indi_ina = stripe.Invoice.retrieve(
                i.billing_id,
            )
            if indi_ina:
                all_invoices.append(indi_ina)
    invoices_all = Invoices.objects.filter(email=user.email)
    indi_in_list = []
    if invoices_all:
        for i in invoices_all:
            indi_in = stripe.Invoice.retrieve(
                i.billing_id,
            )
            if indi_in:
                indi_in_list.append(indi_in)
    lasUsers = UserApp.objects.filter().distinct('user_id')
    a_notifications = Notification.objects.all()
    apps = App.objects.filter(customer_id=user.id)
    notifications = []
    for app in apps:
        all_notifications = Notification.objects.filter(app_id=app.id)
        for noti in all_notifications:
            notifications.append(noti)
    users = UserApp.objects.filter(customer_id=user.id).distinct('user_id')
    # print(users)
    # us = UserApp.objects.all()
    # print(us)   
    app_users_list = []
    userApps = App.objects.filter(customer_id=user.id)
    if userApps:
        for ob in userApps:
            us = UserApp.objects.filter(app_id=ob.id).count()
            mydict = {
                "id": ob.id,
                "name": ob.name,
                "notifications_used": ob.notifications_used,
                "notifications_actual_used":ob.notifications_actual_used,
                "app_qr":ob.app_qr,
                "actual_used":us
            }
            app_users_list.append(mydict)

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



    context = {"app_users_list":app_users_list, "invoice_item":invoice_item, "total_users":total_users, "users":users, "indi_in_list":indi_in_list ,"all_invoices":all_invoices, "a_notifications":a_notifications, "notifications":notifications, "lasUsers":lasUsers, "all_app":all_app,"userApps":userApps,"total_used_notification":total_used_notification,"remaining_notification":remaining_notification,}
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

    def create(self, request, *args, **kwargs):
        get_user_id  = request.data['user_id']
        get_app_id = request.data['app_id']
        get_existing_obj = UserApp.objects.filter(user_id = get_user_id).filter(app_id = get_app_id).last()
        if get_existing_obj is not None:
            return Response({"message": "Already added",  "status": status.HTTP_429_TOO_MANY_REQUESTS})
        else:
            response = super().create(request, *args, **kwargs)
            return Response({"message": "Successfully added",  "status": status.HTTP_201_CREATED})


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



@api_view(['POST'])
def getUserApps(request):
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
            serializer = AppSerializer(user_apps, many=True)
            return JsonResponse(serializer.data, safe=False)
        else:
            return Response({"message": "User does not exixts " , "status": status.HTTP_400_BAD_REQUEST})
    else:
        return Response({"detail": "Invalid Request!",  "status": status.HTTP_400_BAD_REQUEST})


@api_view(['POST'])
def deleteUserApps(request):
    if request.method == 'POST':
        try:
            user_id  = request.data['user_id']
            app_id  = request.data['app_id']
        except MultiValueDictKeyError:
            return Response({"detail": "Make sure user_id and app_id are provided",  "status": status.HTTP_400_BAD_REQUEST})        
        try:
            get_user = User.objects.get(id = user_id)
        except User.DoesNotExist:
            get_user = None
        if get_user is not None:
            # print(get_user.id)
            try:
                get_user_app = UserApp.objects.filter(app_id = app_id).get(user_id = user_id)
            except UserApp.DoesNotExist:
                get_user_app = None
            if get_user_app is not None :
                get_user_app.delete()
                return Response({"message": "Successfully removed", "status": status.HTTP_201_CREATED})
            else:
                return Response({"message": "App is not registered in your account" , "status": status.HTTP_400_BAD_REQUEST})
        else:    
            return Response({"message": "User does not exixts " , "status": status.HTT})
    else:
        return Response({"detail": "Invalid Request!",  "status": status.HTTP_400_BAD_REQUEST})




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
def viewInvoice(request, id):
    invoice_obj = stripe.Invoice.retrieve(
    id,
    )
    invoice_datetime = datetime.fromtimestamp(invoice_obj.created).strftime("%A, %B %d, %Y")
    context = {'invoice_datetime':invoice_datetime, 'invoice_obj': invoice_obj}
    return render(request, 'view-invoice.html', context)

@login_required(login_url="/login/")
def createPlan(request):
    user_email = request.user.email
    invoice_item = Invoices.objects.filter(email=user_email)
    if request.method == "POST":
        # name = request.POST.get('name')
        # price = request.POST.get('price')
        # interval = request.POST.get('interval')
        # notifications = request.POST.get('notification')
        # stripeToken = request.POST.get('stripeToken')
        # apps = request.POST.get('apps')
        # description = request.POST.get('description')
        planName = request.POST.get('planName')
        # plan_list = [name,price,interval,notifications,apps,planid]
        # list1 = list1.split(',')
        # print(url_list,plan_list,stripeToken)
    context = {"invoice_item":invoice_item}
    return render(request, 'my-plan.html', context)

@login_required(login_url="/login/")
def updatePlan(request,planName):
    user_email = request.user.email
    if request.method == 'POST':
        stripeToken = request.POST.get('stripeToken')
        if stripeToken:
            if planName == 'privatePlan':
                name_p = 'private'
                price_p = 1 * 100
                interval_p = 1
                notifications_p = 1000
                apps_p = 1
                planId_p = 'price_1HyhdOCEigeyfTXepWPmWItH'
                des = "You have got {} notifications and {} apps for {} month in ${}.".format(notifications_p,apps_p,interval_p,price_p/100)
                description_p = '$2 one-time every 1000 notifications additional app $10 per month'
                customer = stripe.Customer.create(
                    email=user_email,
                    card = stripeToken,
                    description = des,
                )
                if customer:
                    charge = stripe.Charge.create(
                        amount=price_p,
                        currency="usd",
                        customer=customer.id,
                        description=des,
                    )
                    if charge:
                        subscription = stripe.Subscription.create(
                            customer=customer.id,
                            items=[
                                {"price": planId_p},
                            ],
                            metadata={"planName":name_p,"payment_method":charge.payment_method_details.card.brand},
                        )
                        m = stripe.Charge.retrieve(
                            charge.id,
                            expand=['customer', 'invoice.subscription']
                        )
                        invoice_id = None
                        if m:
                            invoice_id = m.customer.subscriptions.data
                            invoice_id = invoice_id[0].latest_invoice
                        if subscription:
                            invoices = Invoices.objects.create(billing_id=invoice_id, name=subscription.metadata['planName'], price=price_p, interval=interval_p, notifications=notifications_p, apps=apps_p, description=description_p, email=user_email, status=subscription.status, payment_method=charge.payment_method_details.card.brand, charge_id=charge.id, customer_id=customer.id, subscription_id=subscription.id, subscription_created_at=subscription.created, charge_receipt_url=charge.receipt_url)
                            if invoices:
                                return redirect('../../success_pay.html')
            elif planName == 'businessPlan':
                name_b = 'business'
                price_b = 4 * 100
                interval_b = 1
                notifications_b = 5000
                apps_b = 3
                planId_b = 'price_1HyhcrCEigeyfTXe4nMbbrAI'
                description_b = '$8 one-time every 5000 notifications additional app $10 per month'
                des = "You have got {} notifications and {} apps for {} month in ${}.".format(notifications_b,apps_b,interval_b,price_b/100)
                customer = stripe.Customer.create(
                    email=user_email,
                    card = stripeToken,
                    description = des,
                )
                if customer:
                    charge = stripe.Charge.create(
                        amount=price_b,
                        currency="usd",
                        customer=customer.id,
                        description=des,
                    )
                    if charge:
                        subscription = stripe.Subscription.create(
                            customer=customer.id,
                            items=[
                                {"price": planId_b },
                            ],
                            metadata={"planName":name_b, "payment_method":charge.payment_method_details.card.brand},
                        )
                        m = stripe.Charge.retrieve(
                            charge.id,
                            expand=['customer', 'invoice.subscription']
                        )
                        invoice_id = None
                        if m:
                            invoice_id = m.customer.subscriptions.data
                            invoice_id = invoice_id[0].latest_invoice
                        if subscription:
                            invoices = Invoices.objects.create(billing_id=invoice_id, name=subscription.metadata['planName'], price=price_b, interval=interval_b, notifications=notifications_b, apps=apps_b, description=description_b, email=user_email, status=subscription.status, payment_method=charge.payment_method_details.card.brand, charge_id=charge.id, customer_id=customer.id, subscription_id=subscription.id, subscription_created_at=subscription.created, charge_receipt_url=charge.receipt_url)
                            if invoices:
                                return redirect('../../success_pay.html')
            elif planName == 'unlimitedPlan':
                name_u = 'unlimited'
                price_u = 7 * 100
                interval_u = 1
                notifications_u = 1000
                apps_u = 1
                planId_u = 'price_1HyhbxCEigeyfTXeiPwwMEQc'
                description_u = '$2 one-time every 1000 notifications additional app $10 per month'
                des = "You have got {} notifications and {} apps for {} month in ${}.".format(notifications_u,apps_u,interval_u,price_u/100)
                customer = stripe.Customer.create(
                    email=user_email,
                    card = stripeToken,
                    description = des,
                )
                if customer:
                    charge = stripe.Charge.create(
                        amount=price_u,
                        currency="usd",
                        customer=customer.id,
                        description=des,
                    )
                    if charge:
                        subscription = stripe.Subscription.create(
                            customer=customer.id,
                            items=[
                                {"price": planId_u },
                            ],
                            metadata={"planName":name_u ,"payment_method":charge.payment_method_details.card.brand},
                        )
                        m = stripe.Charge.retrieve(
                            charge.id,
                            expand=['customer', 'invoice.subscription']
                        )
                        invoice_id = None
                        if m:
                            invoice_id = m.customer.subscriptions.data
                            invoice_id = invoice_id[0].latest_invoice
                        if subscription:
                            status=subscription.status
                            name=subscription.metadata['planName']
                            payment_method=charge.payment_method_details.card.brand
                            charge_receipt_url = charge.receipt_url
                            invoices = Invoices.objects.create(billing_id=invoice_id, name=name, price=price_u, interval=interval_u, notifications=notifications_u, apps=apps_u, description=description_u, email=user_email, status=status, payment_method=payment_method, charge_id=charge.id, customer_id=customer.id, subscription_id=subscription.id, subscription_created_at=subscription.created, charge_receipt_url=charge_receipt_url)
                            if invoices:
                                return redirect('../../success_pay.html')
    data = {'data': user_email}
    return JsonResponse(data)


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
    invoice_item = Invoices.objects.filter(email=user.email)
    total_users =  UserApp.objects.filter(customer_id=user.id).values('user_id').count()
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
            description = form.cleaned_data.get('description')
            app_logo = form.cleaned_data.get('app_logo')
            app_image = form.cleaned_data.get('app_image')
            try:
                get_custmer = Customer.objects.get(email = user.email)
            except Customer.DoesNotExist:
                get_custmer = None
            if get_custmer is None:
                return Response({"message": "Customer does not exists " , "status": status.HTTP_404_NOT_FOUND})
            else:
                app_obj = App.objects.create(name =app_name, description  = description ,app_image  = app_image, customer_id_id = customer_id, app_logo=app_logo)
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
    context = {"invoice_item":invoice_item ,"total_users":total_users, "form":form,"customer_id":customer_id, "total_used_notification":total_used_notification, "remaining_notification":remaining_notification}
    return render(request, 'add-app.html', context)

@login_required(login_url="/login/")
def updateApp(request, pk):
    user = request.user
    customer_id = user.id
    invoice_item = Invoices.objects.filter(email=user.email)
    total_users =  UserApp.objects.filter(customer_id=user.id).values('user_id').count()
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
    
    context = {"invoice_item":invoice_item ,"total_users":total_users, 'form': form, "msg":msg,"app":app, "total_used_notification":total_used_notification, "remaining_notification":remaining_notification}
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


@login_required(login_url="/login/")
def delete_cUser(request, pk):
    user = User.objects.get(id=pk)
    if request.method == "POST":
        user = User.objects.get(id=pk)
        user.delete()
        return redirect("../../connected-users.html")
    context = {'user': user}
    return render(request, 'delete-cUser.html', context)


@login_required(login_url="/login/")
def view_cUser(request,pk):
    user_det = User.objects.get(id=pk)
    context = {"user_det":user_det}
    return render(request, 'view-cUser.html', context)




@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)


class SuccessView(TemplateView):
    template_name = 'success.html'


class CancelledView(TemplateView):
    template_name = 'cancelled.html'


@csrf_exempt
def create_checkout_session(request):
    if request.method == 'GET':
        try:
            checkout_session = stripe.checkout.Session.create(
                # new
                client_reference_id=request.user.id if request.user.is_authenticated else None,
                success_url=api_base_url + 'success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=api_base_url + 'cancelled/',
                payment_method_types=['card'],
                mode='payment',
                line_items=[
                    {
                        'name': "Notifao Plan",
                        'quantity': 1,
                        'currency': 'usd',
                        'amount': '1000',
                    }
                ]
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})


@csrf_exempt
def stripe_webhook(request):
    print("webhook")

    endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        # print(session)
        # print(session.customer)
        # print(session['data'].price.id)

        line_items = stripe.checkout.Session.list_line_items(session['id'], limit=1)
        m = line_items["data"]
        # for n in m:
        inv = stripe.InvoiceItem.create(
            price="price_1IDv45CEigeyfTXe7YAWSqH6",
            customer=session.customer,
        )
        # print(inv)
        if inv:
            invvoi = stripe.Invoice.create(
                customer=inv.customer,
            )
            # print(invvoi)

    return HttpResponse(status=200)




def forgotPasswordEmail(pk):
    user = Customer.objects.get(id=pk)
    emiladdress = user.email
    path = "{}reset_password/{}/".format(api_base_url, pk)
    SENDER = "Notifao <no-reply@notifao.com>"
    RECIPIENT = emiladdress
    # CONFIGURATION_SET = "ConfigSet"
    AWS_REGION = "us-east-1"
    SUBJECT = "Notifao Password Reset"
    BODY_TEXT = ("Amazon SES Test (Python)\r\n"
             "This email was sent with Amazon SES using the "
             "AWS SDK for Python (Boto)."
            )
    BODY_HTML = """<html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <style>
        @media only screen and (max-width: 700px) {
            .main {
                padding: 30px 20px 40px 20px !important;
                width: 90% !important;
            }
            img {
                width: 150px;
            }
            h1 {
                font-size: 30px !important;
            }
            .link {
                font-size: 12px;
                padding: 0px !important;
                background-color: #fff !important;
                color: #5db6c1 !important;
                text-decoration: underline !important;
            }
            .header {
                font-size: 12px !important;
            }
        }
    </style>
    <body style="background: #eee; font-family: sans-serif; margin: 20px;">
        <div class="main" style="min-width: 500px; width: 60%; background: #fff; padding: 50px 40px 80px 40px; margin: 0px auto;">
            <hr style="border: 1px solid rgb(224, 224, 224);">
            <h2 style="color: #444;">Notifao Password Reset</h2>
            <hr style="border: 1px solid rgb(224, 224, 224);">
            <div class="header" style="font-size: 15px;">
                <div style="display: inline-block; line-height: 22px;">
                    <span><b>Notifao</b> no-reply@notifao.com</span><br>
                    <span>Reply-To: no-reply@notifao.com</span><br>
                    <span>To: """+emiladdress+"""</span><br>
                </div>
            </div>
            <div style="text-align: center; margin-top: 60px; margin-bottom: 80px;">
                <img width="100px" margin-bottom: 60px; src="http://ec2-18-185-137-104.eu-central-1.compute.amazonaws.com:1800/static/assets/images/loginlogo.png" alt="logo"><br><br><br>
                <a class="link" href="""+path+"""
                    style="padding: 20px 40px; background-color: #5db6c1; color: #fff; font-weight: bold; text-decoration: none; border-radius: 50px;">CONTINUE
                    TO RESET</a>
            </div>
            <hr style="border: 1px solid rgb(224, 224, 224); width: 80%;">
        </div>
    </body>
    </html>
            """ 
    CHARSET = "UTF-8"
    client = boto3.client(
        "ses",
        aws_access_key_id="AKIAWRTNEJ5DYFCFSHOV",
        aws_secret_access_key="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",
        region_name="ca-central-1"
    )
    try:
    #Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
            # If you are not using a configuration set, comment or delete the
            # following line
            # ConfigurationSetName=CONFIGURATION_SET,
        )
# Display an error if something goes wrong.	
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])



def registrationEmail(emiladdress):
    SENDER = "Notifao <no-reply@notifao.com>"
    RECIPIENT = emiladdress
    # CONFIGURATION_SET = "ConfigSet"
    AWS_REGION = "us-east-1"
    SUBJECT = "Notifao Registration Email"
    BODY_TEXT = ("Amazon SES Test (Python)\r\n"
             "This email was sent with Amazon SES using the "
             "AWS SDK for Python (Boto)."
            )
    BODY_HTML = """<html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <style>
        @media only screen and (max-width: 700px) {
            .main {
                padding: 30px 20px 40px 20px !important;
                width: 90% !important;
            }
            img {
                width: 150px;
            }
            h1 {
                font-size: 30px !important;
            }
            .link {
                font-size: 12px;
                padding: 0px !important;
                background-color: #fff !important;
                color: #5db6c1 !important;
                text-decoration: underline !important;
            }
            .header {
                font-size: 12px !important;
            }
        }
    </style>
    <body style="background: #eee; font-family: sans-serif; margin: 20px;">
        <div class="main" style="min-width: 500px; width: 60%; background: #fff; padding: 50px 40px 80px 40px; margin: 0px auto;">
            <hr style="border: 1px solid rgb(224, 224, 224);">
            <h2 style="color: #444;">Confirm Your Email.</h2>
            <hr style="border: 1px solid rgb(224, 224, 224);">
            <div class="header" style="font-size: 15px;">
                <div style="display: inline-block; line-height: 22px;">
                    <span><b>Notifao</b> no-reply@notifao.com</span><br>
                    <span>Reply-To: no-reply@notifao.com</span><br>
                    <span>To: """+emiladdress+"""</span><br>
                </div>
            </div>
            <div style="text-align: center; margin-top: 60px; margin-bottom: 80px;">
                <img width="100px" margin-bottom: 60px; src="http://ec2-18-185-137-104.eu-central-1.compute.amazonaws.com:1800/static/assets/images/loginlogo.png" alt="logo"><br><br><br>
                <a class="link" href="""+api_base_url+"""
                    style="padding: 20px 40px; background-color: #5db6c1; color: #fff; font-weight: bold; text-decoration: none; border-radius: 50px;">CONTINUE
                    TO CONFIRM</a>
            </div>
            <hr style="border: 1px solid rgb(224, 224, 224); width: 80%;">
        </div>
    </body>
    </html>
            """ 
    CHARSET = "UTF-8"
    client = boto3.client(
        "ses",
        aws_access_key_id="AKIAWRTNEJ5DYFCFSHOV",
        aws_secret_access_key="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",
        region_name="ca-central-1"
    )
    try:
    #Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
            # If you are not using a configuration set, comment or delete the
            # following line
            # ConfigurationSetName=CONFIGURATION_SET,
        )
# Display an error if something goes wrong.	
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])

# registrationEmail("ali679asghar@gmail.com")






