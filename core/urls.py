# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from django.urls import path, include 
from django.conf import settings
from notifications .views import DeviceViewSet
from rest_framework import routers
from django.conf.urls.static import static


# router = routers.DefaultRouter()
# router.register('devices', FCMDeviceAuthorizedViewSet)

router = routers.DefaultRouter()
router.register(r'devices', DeviceViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("authentication.urls")), 
    path("", include("app.urls")),
    path('', include('customers.urls')),
    path('', include('plans.urls')),
    path('', include('users.urls')),
    path('', include('notifications.urls')),
    path('', include(router.urls)),
    # path('', include('invoices.urls')),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG: # new
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
