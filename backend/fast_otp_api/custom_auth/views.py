from django.shortcuts import render
from django.conf import settings

from rest_framework import generics, status as restStatus
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

# relative path
from .models import User, Otp
from .serializers import UserSerializer
from .helper import generte_otp, is_verified
from .helper import SMSVerification

# Create your views here.
import os


@api_view(["POST"])
def send_otp(request):
    """Send opt using Phone verification service"""
    if not request.data.get("phone_number"):
        return Response(
            {"phone_number": ["This field is required"]},
            status=restStatus.HTTP_400_BAD_REQUEST,
        )
    # otp_code = generte_otp(request.data.get("phone_number"))
    smsVerification = SMSVerification()
    status = smsVerification.send_otp(request.data.get("phone_number"))
    return Response({"message": "otp sent to your phone number", "status": status})


@api_view(["POST"])
def verify_otp_create_user(request):
    """verify phone number with otp send through Phone verification service"""
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
    else:
        user, _ = User.objects.update_or_create(
            defaults={"is_verified": True, "is_staff": True},
            phone_number=request.data.get("phone_number"),
        )
        refresh: RefreshToken = RefreshToken.for_user(user)
        return Response(
            {"refresh": str(refresh), "access": str(refresh.access_token)},
            status=restStatus.HTTP_200_OK,
        )


class UserGenericView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
