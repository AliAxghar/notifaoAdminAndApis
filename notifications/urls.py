from django.urls import path, include
from .views import NotificationViewSet
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from .views import DeviceViewSet ,createNotification ,getUserNotifications ,UserNotificationViewSet


router = routers.DefaultRouter()
router.register('notifications', NotificationViewSet)
router.register('user_notifications', UserNotificationViewSet)

urlpatterns = [
   
    path('', include(router.urls)),
    path('getUserNotification/', view = getUserNotifications, name='get_user_notification'),
    path('notifications/create',view = createNotification, name='custom_create_notification'),
    
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
