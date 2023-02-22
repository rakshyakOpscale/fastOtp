from django.conf import settings

# ///////////////////Third parth wrapper////////////////////////////
from twilio.rest import Client


class SMSVerification:
    """A sms wrapper class to use 3rd parth sms service"""

    def __init__(self) -> None:
        self.__account_sid = settings.TWILIO_SID
        self.__auth_token = settings.TWILIO_AUTH_TOKEN
        self.__verify_sid = settings.TWILIO_VERIFY_SID

        self.__client = Client(self.__account_sid, self.__auth_token)
        pass

    def send_otp(self, phone_number: str) -> str:
        """accept to phone_number as string and return verification status"""
        verification = self.__client.verify.v2.services(
            self.__verify_sid
        ).verifications.create(to=f"+91{phone_number}", channel="sms")
        return verification.status

    def verification_check(self,phone_number, otp_code: str) -> bool:
        """takes otp_code as string and return verification check status"""
        verification_check = self.__client.verify.v2.services(
            self.__verify_sid
        ).verification_checks.create(to=f"+91{phone_number}", code=otp_code)
        return True if verification_check.status == "approved" else False 