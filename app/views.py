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
from apps.models import *

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