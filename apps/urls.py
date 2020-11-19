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

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)