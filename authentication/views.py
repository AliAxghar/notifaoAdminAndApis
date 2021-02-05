# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.forms.utils import ErrorList
from django.http import HttpResponse
from .forms import LoginForm, SignUpForm
from django.http import JsonResponse
from customers.models import Customer
from core.settings import api_base_url
import requests
def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:    
                msg = 'Email or password is incorrect'    
        else:
            msg = 'Error validating the form'    

    return render(request, "accounts/login.html", {"form": form, "msg" : msg})

# def register_user(request):

#     msg     = None
#     msg1     = None
#     success = False

#     if request.method == "POST":
#         phone = request.POST.get('phone_number')
#         name = request.POST.get('name')
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         password2 = request.POST.get('password2')
#         get_customer_email = Customer.objects.filter(email=email)
#         get_customer_phone = Customer.objects.filter(phone=phone)
#         if get_customer_email:
#             msg = "User is already exist with this email"
#         else:
#             if get_customer_phone:
#                 msg = "This phone number is already exist"
#             else:
#                 if password==password2:
#                     if len(password) < 8:
#                         msg = "Password is too short, must contain at least 8 characters."
#                     else:
#                         data = {"name":name, "phone":phone, "email":email, "password1":password, "password2":password, "business_name":"None"}
#                         createCustomer = requests.post('{}customer/register/'.format(api_base_url), data=data)
#                         res = createCustomer.json()
#                         pass_validate = res
#                         if res:
#                             if len(res) > 1:
#                                 return redirect('/login/')
#                             else:
#                                 msg = "This password is too common."
#                         # customer = Customer.objects.create(name=name, phone=phone, email=email, password=password)                            
#                 else:
#                     msg = "Passwords do not match"

#     return render(request, "accounts/register.html", {"msg" : msg, "success" : success })


def register_user(request):

    msg = None
    msg1 = None
    success = False
    # if request.method == "POST":
    # phone = request.POST.get('phone_number')
    # name = request.POST.get('name')
    # email = request.POST.get('email')
    # password = request.POST.get('password')
    # password2 = request.POST.get('password2')
    userdatalist = request.GET.getlist('list[]')
    if userdatalist:
        name = userdatalist[0]
        email = userdatalist[1]
        phone = userdatalist[2]
        password = userdatalist[3]
        password2 = userdatalist[4]
        terms = userdatalist[5]
        # print(name,email,phone,password,password2)
        get_customer_email = Customer.objects.filter(email=email)
        get_customer_phone = Customer.objects.filter(phone=phone)
        if get_customer_email:
            msg = "User is already exist with this email"
        else:
            if terms == "No":
                msg = "Please agree to terms and conditions"
            else:
                if password==password2:
                    if len(password) < 8:
                        msg = "Password is too short, must contain at least 8 characters."
                    else:
                        data = {"name":name, "phone":phone, "email":email, "password1":password, "password2":password, "business_name":"None"}
                        createCustomer = requests.post('{}customer/register/'.format(api_base_url), data=data)
                        res = createCustomer.json()
                        pass_validate = res
                        if res:
                            if len(res) > 1:
                                success = True
                                msg = "User created successfully"
                            else:
                                msg = "This password is too common."
                        # customer = Customer.objects.create(name=name, phone=phone, email=email, password=password)                            
                else:
                    msg = "Passwords do not match"
        data = { 'msg': msg, "msg1":msg1, 'data': userdatalist }
        return JsonResponse(data)

    return render(request, "accounts/register.html", {"msg" : msg, "success" : success })