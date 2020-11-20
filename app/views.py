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

@login_required(login_url="/login/")
def index(request):
    
    context = {}
    context['segment'] = 'index'

    html_template = loader.get_template( 'index.html' )
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def pages(request):
    context = {}
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