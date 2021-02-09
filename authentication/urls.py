# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path
from .views import login_view, register_user, reset_password
from django.contrib.auth.views import LogoutView
from .views import *

urlpatterns = [
    path('login/', login_view, name="login"),
    path('register/', register_user, name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path('reset/', reset_view, name="reset"),
    path('reset_password/<str:pk>/',reset_password, name="reset_password"),
]
