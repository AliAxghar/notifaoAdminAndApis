from django.shortcuts import render
from rest_framework import viewsets
from .models import User
from .serializers import UserSerializer
from rest_framework .decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework import status
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from core.settings import api_base_url
import boto3
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer



@api_view(['POST'])
def customUserRegister(request):
    if request.method == 'POST':
        try:
            user_email  = request.data['email']
            user_name = request.data['name']
            # user_phone = request.data['phone']
        except MultiValueDictKeyError:
            return Response({"detail": "Make sure all perameters (email,password,name,phone,profile_image) are provided",  "status": status.HTTP_400_BAD_REQUEST})        
        try:
            get_user = User.objects.get(email = user_email)
        except User.DoesNotExist:
            get_user = None
        if get_user is None:
            
            user_obj = User.objects.create(name =user_name, email = user_email )
            user_obj.save()
            registrationEmail(user_email)
            if user_obj is not None:
                return Response({"message": user_obj.id, "status": status.HTTP_201_CREATED})
            else:
                return Response({"message": "User not created" , "status": status.HTTP_406_NOT_ACCEPTABLE})
            
        else:
            return Response({"message": "Email already exists " , "status": status.HTTP_306_RESERVED})
    else:
        return Response({"detail": "Invalid Request!",  "status": status.HTTP_400_BAD_REQUEST})
    


@api_view(['POST'])
def custom_user_login(request):
    if request.method == 'POST':
        user_email  = request.data['email']
        user_password = request.data['password']
       
        try:
            get_custmer = User.objects.get(email = user_email)
        except User.DoesNotExist:
            get_custmer = None
        if get_custmer is None:
            return Response({"detail": "user does not exist",  "status": status.HTTP_404_NOT_FOUND})
        else:
            if get_custmer.password == user_password:
                return Response({
                    "id": get_custmer.id,
                    "name": get_custmer.name,
                    "email": get_custmer.email,
                    "phone": get_custmer.phone,
                    "profile_pic": get_custmer.profile_pic ,
                })
            else:
                return Response({"detail": "Invalid password",  "status": status.HTTP_401_UNAUTHORIZED})
                        
    else:
        return Response({"detail": "Invalid Request!",  "status": status.HTTP_400_BAD_REQUEST})
   
def registrationEmail(emiladdress):
    SENDER = "Notifao <no-reply@notifao.com>"
    RECIPIENT = emiladdress
    # CONFIGURATION_SET = "ConfigSet"
    AWS_REGION = "us-east-1"
    SUBJECT = "Notifao Registration Email"
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
            
            <hr style="border: 1px solid rgb(224, 224, 224);">
            <div class="header" style="font-size: 15px;">
                <div style="display: inline-block; line-height: 22px;">
                    <span><b>Notifao</b> no-reply@notifao.com</span><br>
                    <span>Reply-To: no-reply@notifao.com</span><br>
                    <span>To: """+emiladdress+"""</span><br>
                </div>
            </div>
            <div style="text-align: center; margin-top: 60px; margin-bottom: 80px;">
                <img width="100px" margin-bottom: 60px; src="http://ec2-18-185-137-104.eu-central-1.compute.amazonaws.com:1800/static/assets/images/loginlogo.png" alt="logo"><br><br><br>
                <h2 style="color: #444;">Successfully Registered.</h2><br><br>
                <p style="text-align:center;font-size:18px;font-weight:500;">If you did not request this """+emiladdress+""" be registered in Notifao, please ignore this email.</p>
            </div>
            <hr style="border: 1px solid rgb(224, 224, 224); width: 80%;">
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