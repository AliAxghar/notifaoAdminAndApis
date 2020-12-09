from django.urls import path, include
from .views import PlanViewSet ,addPlan
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers



router = routers.DefaultRouter()
router.register('plans', PlanViewSet)

urlpatterns = [
   
    path('', include(router.urls)),
    path('plan/addplan', addPlan)
    
]
