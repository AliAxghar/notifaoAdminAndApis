from django.urls import path, include
from .views import UserViewSet , customUserRegister ,custom_user_login
from django.conf import settings
from django.conf.urls.static import static
from app.views import *
from rest_framework import routers



router = routers.DefaultRouter()
router.register('users', UserViewSet)

urlpatterns = [
   
    path('', include(router.urls)),
    path('users/customUserRegister', view = customUserRegister, name='customRegister'),
    path('users/customUserLogin', view = custom_user_login, name='custom_user_login'),

    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)