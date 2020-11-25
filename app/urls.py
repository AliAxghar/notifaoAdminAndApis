# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from app import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from .views import AppViewSet , createApp, UserAppViewSet
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers

router = routers.DefaultRouter()
router.register('apps', AppViewSet)
router.register('userapp', UserAppViewSet)


urlpatterns = [
   
    path('', include(router.urls)),
    path('apps/createapp/', view = createApp, name='create_app'),
    
]

urlpatterns = [
    # Matches any html file - to be used for gentella
    # Avoid using your .html in your resources.
    # Or create a separate django app.
    re_path(r'^.*\.html', views.pages, name='pages'),

    # The home page
    path('', views.index, name='home'),
    path('update_profile/<str:pk>/', views.updateProfile, name="update_profile"),
    path('create_apps/', views.create_apps, name="create_apps"),
    path('view_apps/<str:pk>/', views.view_apps, name="view_apps"),

    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
