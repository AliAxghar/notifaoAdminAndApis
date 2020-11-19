from django.shortcuts import render
from .models import Plan
from customers .models import Customer
from .serializers import PlanSerializer
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from plans .models import Plan



class PlanViewSet(viewsets.ModelViewSet):
    
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer


@api_view(['GET', 'POST'])
def addPlan(request):
    if request.method == 'POST':
        plan_id = request.data['planid']
        user_id = request.data['uid']
        
        # user = CustomUser.objects.get(phone=requestPhone)
        try:
            get_user = Customer.objects.get(id = user_id)
        except Customer.DoesNotExist:
            get_user = None
        # print(go)
        if get_user is None:
            
            return Response({"message": "Customer does not exist " , "status": status.HTTP_409_CONFLICT})
        else :
            try:
                selected_plan = Plan.objects.get(id = plan_id)
            except Plan.DoesNotExist:
                selected_plan = None
        # print(go)
            if selected_plan is None:
                return Response({"message": "Plan does not exist " , "status": status.HTTP_409_CONFLICT})
            else:
                get_user.push_notifications = selected_plan.notifications
                get_user.apps_allowed = selected_plan.apps
                get_user.save()
                return Response({"message": "Plan successfully added" , "status": status.HTTP_200_OK})
    else:
        return Response({"detail": "Invalid Request!",  "status": status.HTTP_400_BAD_REQUEST})
