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
import boto3
# from rest_auth.registration.views import RegisterView, VerifyEmailView
from .serializers import CustomerSerializer
from rest_auth.views import LoginView
from botocore.exceptions import ClientError

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
    

def sendEmail(emiladdress,name):
    print(emiladdress)
    print("/////////////send email is called")
    SENDER = " Notifao <no-reply@notifao.com>"
    RECIPIENT = emiladdress
    # CONFIGURATION_SET = "ConfigSet"
    AWS_REGION = "us-east-1"
    SUBJECT = "Griplay reminder notification"
    BODY_TEXT = ("Amazon SES Test (Python)\r\n"
             "This email was sent with Amazon SES using the "
             "AWS SDK for Python (Boto)."
            )

    BODY_HTML = """<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<style>
    @media only screen and (max-width: 700px) {
        .main {
            padding: 30px 20px 40px 20px !important;
            width: 90% !important;
        }
        img {
            width: 150px;
        }
        h1 {
            font-size: 30px !important;
        }
        .link {
            font-size: 12px;
            padding: 0px !important;
            background-color: #fff !important;
            color: #5db6c1 !important;
            text-decoration: underline !important;
        }
        .header {
            font-size: 12px !important;
        }
    }
</style>
<body style="background: #eee; font-family: sans-serif; margin: 20px;">
    <div class="main" style="min-width: 500px; width: 60%; background: #fff; padding: 50px 40px 80px 40px; margin: 0px auto;">
        <hr style="border: 1px solid rgb(224, 224, 224);">
        <h2 style="color: #444;">Hi """+name+"""! Don't lose your daily input streak.</h2>
        <hr style="border: 1px solid rgb(224, 224, 224);">
        <div class="header" style="font-size: 15px;">
            <div style="display: inline-block; line-height: 22px;">
                <span><b>Gripaly</b> day-by-day@gripaly.com</span><br>
                <span>Reply-To: no-reply@gripaly.com</span><br>
                <span>To: """+emiladdress+"""</span><br>
            </div>
        </div>
        <div style="text-align: center; margin-top: 60px; margin-bottom: 80px;">
            <img width="250px" src="http://3.18.225.181:2100/static/images/logo.png" alt="logo">
            <h1 style="font-size: 50px; color: #444;">Daily Griplay Reminder!</h1>
            <p style="line-height: 22px; color: #666; margin-bottom: 50px;">Hi """+name+""", Don't miss any day. Use gripaly
                today <br> to feel
                better day by day.</p>
            <a class="link" href="https://gripaly.com/"
                style="padding: 20px 40px; background-color: #5db6c1; color: #fff; font-weight: bold; text-decoration: none; border-radius: 50px;">CONTINUE
                USING GRIPALY</a>
        </div>
        <hr style="border: 1px solid rgb(224, 224, 224); width: 80%;">
        <address style="text-align: center; margin-top: 30px; color: #666;">Sydney, Australia</address>
        <!-- <p style="text-align: center; margin-top: 30px; color: #666;">Social Links</p> -->
    </div>
</body>
</html>
            """ 
    CHARSET = "UTF-8"
    client = boto3.client(
        "ses",
        aws_access_key_id="AKIAWRTNEJ5DYFCFSHOV",
        aws_secret_access_key="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",
        region_name="ca-central-1"
    )
    try:
    #Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
            # If you are not using a configuration set, comment or delete the
            # following line
            # ConfigurationSetName=CONFIGURATION_SET,
        )
# Display an error if something goes wrong.	
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])
sendEmail("ali679asghar@gmail.com","Ali")