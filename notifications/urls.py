from django.urls import path, include
from .views import NotificationViewSet
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from .views import DeviceViewSet


router = routers.DefaultRouter()
router.register('notifications', NotificationViewSet)

urlpatterns = [
   
    path('', include(router.urls)),
    
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
