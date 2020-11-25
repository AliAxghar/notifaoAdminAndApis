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
import time
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

@login_required(login_url="/login/")
def index(request):
    
    context = {}
    context['segment'] = 'index'

    html_template = loader.get_template( 'index.html' )
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def pages(request):
    all_app = App.objects.all()
    context = {"all_app":all_app}
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
                    app_obj = App.objects.create(name =app_name, description  = app_description ,app_image  = image_app , customer_id = get_custmer)
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
def updateProfile(request, pk):
    msg = ""
    user = Customer.objects.get(id=pk)
    form = UpdateProfileForm(request.POST or None, request.FILES or None,instance=user)
    if request.method == 'POST':
        form = UpdateProfileForm(request.POST or None, request.FILES or None, instance=user)
        # print(request.FILES)
        if form.is_valid():
            user = form.save()
            password = form.cleaned_data.get('New_password')
            if password:
                user.set_password(password)
            user.save()
            msg = "Profile updated successfully"
            time.sleep(2)
            # return redirect("update_profile/<str:pk>/") 	
            context = {'form': form, "msg":msg}
            return render(request, 'profile.html', context)
            # return redirect("/") 		    										
    
    context = {'form': form, "msg":msg}
    return render(request, 'profile.html', context)

@login_required(login_url="/login/")
def create_apps(request):
    user = request.user
    if request.method == 'POST':
        app_name  = request.POST.get('app_name')
        app_url  = request.POST.get('app_url')
        app_description  = request.POST.get('app_description')
        app_logo  = request.POST.get('app_logo')
        app_back  = request.POST.get('app_back')
        app_obj = App.objects.create(name =app_name, description  = app_description ,app_url  = app_url, app_logo = app_logo, app_image=app_back, customer_id = user)
        if app_obj:
            return redirect("../../app.html")
    context = {}
    return render(request, 'add-app.html', context)


@login_required(login_url="/login/")
def view_apps(request,pk):
    app_detail = App.objects.get(id=pk)
    context = {"app_detail":app_detail}
    return render(request, 'view-app.html', context)
