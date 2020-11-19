from django.urls import path, include
from .views import CustomerViewSet, CustomRegisterView, CustomLoginView

from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers


router = routers.DefaultRouter()
router.register('customers', CustomerViewSet)

urlpatterns = [
   
    # path('user/login/', CustomAuthToken.as_view()),
    path('rest-auth/', include('rest_auth.urls')),
    path('customer/register/', CustomRegisterView.as_view(), name='my_custom_register'),
    path('customer/login/', CustomLoginView.as_view(),  name='my_custom_login'),
    path('', include(router.urls))
    
]
