from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

# relative path
from .models import User, Otp
from .serializers import UserSerializer, OTPSerializer
from .helper import generte_otp, is_verified
import random

# Create your views here.


@api_view(["POST"])
def send_otp(request):
    if not request.data.get("phone_number"):
        return Response({"phone_number": ["This field is required"]})
    otp_code = generte_otp(request.data.get("phone_number"))
    return Response({"otp_code": otp_code})


@api_view(["POST"])
def verify_otp(request):
    if is_verified(request.data):
        return Response({"message": "verification is successfull"})
    return Response({"error": "verification failed"}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)


class UserGenericView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
