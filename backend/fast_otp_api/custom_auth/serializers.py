from rest_framework import serializers

from .models import User, Otp


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["phone_number"]


class OTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = Otp
        fields = ["otp_code", "expire_time", "phone_number"]
