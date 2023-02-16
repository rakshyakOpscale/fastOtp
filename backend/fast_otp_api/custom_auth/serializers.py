from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.db.utils import IntegrityError


from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken, UntypedToken

from twilio.rest import TwilioException

from .models import User, Otp
from .helper import SMSVerification


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "phone_number"]


class OTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = Otp
        fields = ["otp_code", "expire_time", "phone_number"]


class SendOtpSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    status = serializers.CharField(read_only=True)
    message = serializers.CharField(read_only=True)

    def create(self, validated_data):
        try:
            status = SMSVerification().send_otp(validated_data["phone_number"])
            validated_data["status"] = status
            validated_data["message"] = "Opt sent to your phone number"
            return {**validated_data}
        except Exception:
            msg = "Cannot create User"
            raise serializers.ValidationError(msg, code="unique_user_constraint")


class OtpVerifySerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    otp_code = serializers.CharField(write_only=True)
    status = serializers.CharField(read_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    def validate(self, attrs):
        phone_number = attrs.get("phone_number")
        otp_code = attrs.get("otp_code")
        try:
            status = SMSVerification().verification_check(phone_number, otp_code)
            if status is False:
                raise serializers.ValidationError
            attrs.setdefault("status", status)
        except serializers.ValidationError:
            msg = {"otp_code": "Otp verification vailed"}
            raise serializers.ValidationError(msg, code="otp_code")
        except TwilioException as e:
            print({"SMSVerification_error": e})
        try:
            user = User.objects.get(phone_number=phone_number)
            refresh, access = self.get_access_token(user)
            attrs.setdefault("access", access)
            attrs.setdefault("refresh", refresh)
        except User.DoesNotExist:
            user = User.objects.create_user(
                phone_number=phone_number,
                password=make_password(phone_number),
                is_verified=True,
            )
            user.save()
        return attrs

    def create(self, validated_data):
        return {**validated_data}

    def get_access_token(self, user) -> tuple:
        refresh = RefreshToken().for_user(user)
        access = refresh.access_token
        return refresh, access


# class JwtTokeObtainSerializer(serializers.Serializer):
#     phone_number = serializers.CharField()

#     def validate(self, attrs):
#         phone_number = attrs.get("phone_number")
#         password = attrs.get("password")

#         if phone_number:
#             user = authenticate(
#                 request=self.context.get("request"),
#                 phone_number=phone_number,
#             )
#             if not user:
#                 msg = "Unable to log in with provided credentials."
#                 raise serializers.ValidationError(msg, code="authorization")
#         else:
#             msg = "Must include 'phone_number'"
#             raise serializers.ValidationError(msg, code="authorization")
#         refresh = self.get_token(user)
#         data = {"refresh": str(refresh), "access": str(refresh.access_token)}
#         return data


class JwtTokenVerifySerializer(serializers.Serializer):
    token = serializers.CharField()

    def validate_token(self, token):
        try:
            UntypedToken(token)
        except Exception:
            msg = "Token is invalid or expired"
            raise serializers.ValidationError(msg, code="token_not_valid")

        try:
            AccessToken(token)
        except Exception:
            msg = "Token is not an access token"
            raise serializers.ValidationError(msg, code="not_access_token")
        return token

    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)
