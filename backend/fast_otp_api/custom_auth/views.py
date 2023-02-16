from django.shortcuts import render
from django.conf import settings
from django.contrib.auth import logout

from rest_framework import viewsets, status as restStatus, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenVerifyView

# relative path
from .models import User
from .helper import SMSVerification
from .serializers import UserSerializer, JwtTokenVerifySerializer, SendOtpSerializer, OtpVerifySerializer

# Create your views here.


class SendOtpViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = User.objects.all()
    serializer_class = SendOtpSerializer

class OtpVerifyViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = User.objects.all()
    serializer_class = OtpVerifySerializer


# @api_view(["POST"])
# def send_otp(request):
#     """Send opt using Phone verification service"""
#     if not request.data.get("phone_number"):
#         return Response(
#             {"phone_number": ["This field is required"]},
#             status=restStatus.HTTP_400_BAD_REQUEST,
#         )
#     # otp_code = generte_otp(request.data.get("phone_number"))
#     smsVerification = SMSVerification()
#     status = smsVerification.send_otp(request.data.get("phone_number"))
#     return Response({"message": "otp sent to your phone number", "status": status})

# @api_view(["POST"])
# @permission_classes([permissions.AllowAny])
# def verify_otp_create_user(request):
#     """verify phone number with otp send through Phone verification service"""
#     serializer = OtpVerifySerializer(data=request.data)
#     serializer.is_valid(raise_exception=True)
#     return Response(serializer.data)


# @api_view(["GET", "POST"])
# def login_user(request):
#     # TODO:change pk to jwt access token
#     return Response({"detail": "jwt token"})


@api_view(["GET"])
def log_out_user(request):
    logout(request)
    return Response(
        {"detail": "user logged out"},
        status=restStatus.HTTP_200_OK,
    )


# class JwtTokenObtainView(TokenObtainPairView):
#     serializer_class = JwtTokeObtainSerializer


class JwtTokenVerifyView(TokenVerifyView):
    serializer_class = JwtTokenVerifySerializer


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
