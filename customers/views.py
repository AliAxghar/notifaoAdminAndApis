from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated 
from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import CreateAPIView 
from .models import Customer
from rest_auth.registration.views import RegisterView, VerifyEmailView
from rest_framework import status
# from rest_auth.registration.views import RegisterView, VerifyEmailView
from .serializers import CustomerSerializer
from rest_auth.views import LoginView




class CustomerViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


    
class CustomRegisterView(RegisterView):
    swagger_schema = None
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        custom_data = {"message": "Customer has been registered", "status": True}
        response.data.update(custom_data)
        return response


class CustomLoginView(LoginView):

    def get_response(self):
        orginal_response = super().get_response()
        original_dict = dict()
        user_dict = dict()
        original_dict = orginal_response.data
        # print(orginal_response.data ['user'])
        # user_dict = original_dict['user']
        # uid = (user_dict['id'])
        # paid_user = (user_dict['paid_user'])
        # sub_key = (user_dict['stripe_subscription'])
        # start = date.today()
        # created_at = user_dict['payment_date']
        # dt = datetime.strptime(created_at,"%Y-%m-%d")
        # if paid_user == True and sub_key :
        #     stripe.api_key = "sk_test_1PVePrxxxxPJIgZJBctWMaLk00rzthtpvN"
        #     sub_obj = stripe.Subscription.retrieve(sub_key,)
        #     if sub_obj:
        #         if sub_obj['status'] != 'active' :
        #             print(sub_obj['status'])
        #             user_dict['paid_user'] = False
        #             original_dict['user'] = user_dict
        #             t = CustomUser.objects.get(id=uid)
        #             t.paid_user = False  # change field
        #             t.save()

        # if paid_user == True :
        #     start = datetime.now().date()
        #     delta = start - payment_date.date()
        #     difference_30 = delta / timedelta(days=30)
        #     difference_180 = delta / timedelta(days= 180)
        #     difference_7 = delta / timedelta(days=7 )

        #     if difference_21 >= 1:
        #         flag_21 = True




        mydata = {"message": "User has been Logged In.", "status": True, }        
        orginal_response.data.update(mydata)
        return orginal_response