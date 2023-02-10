from django.shortcuts import render
from rest_framework import generics, status as restStatus
from rest_framework.decorators import api_view
from rest_framework.response import Response

# relative path
from .models import User, Otp
from .serializers import UserSerializer, OTPSerializer
from .helper import generte_otp, is_verified
from .helper import SMSVerification
import random

# Create your views here.


@api_view(["POST"])
def send_otp(request):
    if not request.data.get("phone_number"):
        return Response({"phone_number": ["This field is required"]})
    # otp_code = generte_otp(request.data.get("phone_number"))
    smsVerification = SMSVerification()
    status = smsVerification.send_otp(request.data.get("phone_number"))
    return Response({"message": "otp sent to your phone number", "status": status})


@api_view(["POST"])
def verify_otp(request):
    smsVerification = SMSVerification()
    status = smsVerification.verification_check(
        request.data.get("phone_number"), request.data.get("otp_code")
    )
    if status is False:
        return Response(
            {
                "error": f"Otp did not match for phone number {request.data.get('phone_number')}",
                "status": "pending",
            },
            status=restStatus.HTTP_400_BAD_REQUEST,
        )
    return Response({"message": f"phone number {request.data.get('phone_number')} is verified","status": "approved"}, status=restStatus.HTTP_200_OK)


class UserGenericView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
