from django.urls import path, re_path
from app import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from users.models import User
from notifications.views import *

router = routers.DefaultRouter()
router.register('apps', AppViewSet),
router.register('userapp', UserAppViewSet)

urlpatterns = [
    path('', views.index, name='home'),
    path('', include(router.urls)),
    path('createapp/', view = createApp, name='create_app'),
    path('getUserApps/', view = getUserApps, name='get_user_apps'),
    path('deleteUserApp/', view = deleteUserApps, name='delete_user_app'),

    re_path(r'^.*\.html', views.pages, name='pages'),
    path('update_profile/<str:pk>/', views.updateProfile, name="update_profile"),
    path('updateApp/<str:pk>/', views.updateApp, name="updateApp"),
    path('deleteApp/<str:pk>/', views.deleteApp, name="deleteApp"),
    path('create_apps/', views.create_apps, name="create_apps"),
    path('view_apps/<str:pk>/', views.view_apps, name="view_apps"),
    path('singleNotification/<str:pk>/', views.singleNotification, name="singleNotification"),
    path('deleteNotification/<str:pk>/', views.deleteNotification, name="deleteNotification"),
    path('viewInvoice/<str:id>/', views.viewInvoice, name="viewInvoice"),
    path('createPlan/', views.createPlan, name="createPlan"),
    path('createNotificationDashboard/', views.createNotificationDashboard, name="createNotificationDashboard"),
    path('updatePlan/<str:planName>/', views.updatePlan, name="updatePlan"),
    path('delete_cUser/<str:pk>/', views.delete_cUser, name="delete_cUser"),
    path('email_verification/<str:pk>/', views.email_verification, name="email_verification"),
    path('view_cUser/<str:pk>/', views.view_cUser, name="view_cUser"),
    path('config/', views.stripe_config, name="config"),
    path('create-checkout-session/', views.create_checkout_session, name="create-checkout-session"),
    path('success/', views.SuccessView.as_view()),
    path('cancelled/', views.CancelledView.as_view()),
    path('webhook/', views.stripe_webhook, name="webhook"),


    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG: 
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
