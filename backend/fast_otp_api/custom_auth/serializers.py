from django.contrib.auth.hashers import make_password
from django.contrib.auth import login

from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken, UntypedToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import TokenError

from twilio.rest import TwilioException

from .models import User, Otp
from .helper import SMSVerification
from user.models import Profile

jwt_authentication = JWTAuthentication()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "phone_number"]


class OTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = Otp
        fields = ["otp_code", "expire_time", "phone_number"]


class SendOtpSerializer(serializers.Serializer):
    """send otp to the phone number using Sms service"""

    phone_number = serializers.CharField()
    status = serializers.CharField(read_only=True)
    message = serializers.CharField(read_only=True)

    def create(self, validated_data):
        try:
            status = SMSVerification().send_otp(validated_data["phone_number"])
            validated_data["status"] = status
            validated_data["message"] = "Opt sent to your phone number"
            return {**validated_data}
        except TwilioException:
            msg = "Sms service failed"
            raise serializers.ValidationError(msg, code="failed_sms_service")


class OtpVerifySerializer(serializers.Serializer):
    """
    1. Verify otp for the phone number
    2. if the user not exist,create the user
    3. generate access and refresh token
    """

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
        except serializers.ValidationError:
            msg = {"otp_code": "Otp verification vailed"}
            raise serializers.ValidationError(msg, code="otp_code")
        except TwilioException as e:
            print({"SMSVerification_error": e})
            return serializers.ValidationError(
                {"detail": "SMSservice failed", "message": e}
            )
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
            Profile.objects.create(user=user).save()
            refresh, access = self.get_access_token(user)
            attrs.setdefault("access", access)
            attrs.setdefault("refresh", refresh)
        return attrs

    def create(self, validated_data):
        return {**validated_data}

    def get_access_token(self, user: User) -> tuple:
        """return tuple (refresh, access)"""
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
    """Verify and login the user if the token is valid"""

    token = serializers.CharField()

    def validate_token(self, token):
        try:
            UntypedToken(token)
        except TokenError:
            msg = "Token is invalid or expired"
            raise serializers.ValidationError(msg, code="token_not_valid")

        try:
            validated_token = AccessToken(token)
            user = jwt_authentication.get_user(validated_token)
            login(self.context["request"], user)
        except TokenError:
            msg = "Not an access token"
            raise serializers.ValidationError(msg, code="not_acces_token")
        return token
