
from django.urls import path, re_path
from app import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers

router = routers.DefaultRouter()
router.register('apps', AppViewSet),
router.register('userapp', UserAppViewSet)

urlpatterns = [
    path('', views.index, name='home'),
    path('', include(router.urls)),
    path('createapp/', view = createApp, name='create_app'),

    re_path(r'^.*\.html', views.pages, name='pages'),
    path('update_profile/<str:pk>/', views.updateProfile, name="update_profile"),
    path('updateApp/<str:pk>/', views.updateApp, name="updateApp"),
    path('deleteApp/<str:pk>/', views.deleteApp, name="deleteApp"),
    path('create_apps/', views.create_apps, name="create_apps"),
    path('view_apps/<str:pk>/', views.view_apps, name="view_apps"),
    path('singleNotification/<str:pk>/', views.singleNotification, name="singleNotification"),

    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG: 
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
