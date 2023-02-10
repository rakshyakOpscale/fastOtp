from .models import Otp, User

import random
from django.http import HttpRequest


# ///////////////////Third parth wrapper////////////////////////////
import os
from twilio.rest import Client


class SMSVerification:
    """A sms wrapper class to use 3rd parth sms service"""

    def __init__(self) -> None:
        self.__account_sid = (
            os.environ.get("TWILLO_SID") or "ACf3938be855012233c39a7c41392b63c9"
        )
        self.__auth_token = (
            os.environ.get("TWILLO_AUTH_TOKEN") or "d691ce77dcfdacb37abe8ecb4b7552b4"
        )
        self.__verify_sid = (
            os.environ.get("TWILLO_VERIFY_SID") or "VA1834fecbaadffe551b3324f37bbc27d4"
        )

        self.__client = Client(self.__account_sid, self.__auth_token)
        pass

    def send_otp(self, phone_number: str) -> str:
        """accept to phone_number as string and return verification status"""
        self.__verified_number = phone_number
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


# ///////////////////methods////////////////////////////
def generte_otp(phone_number: str) -> str:
    """creates entry in the database and return otp_code"""
    instance, is_created = Otp.objects.update_or_create(
        defaults={
            "otp_code": random.randint(10000, 99999),
        },
        phone_number=phone_number,
    )
    return instance.otp_code


def is_verified(data: HttpRequest) -> bool:
    """
    data{
        phone_number: str,
        otp_code: str,
    }
    """
    if isinstance(data, HttpRequest):
        raise ValueError("data is not instance of HttpRequest")
    otp = Otp.objects.get(phone_number=data.get("phone_number"))
    if data.get("otp_code") == otp.otp_code:
        User.objects.update_or_create(
            defaults={"is_verified": True, "is_staff": True},
            phone_number=data.get("phone_number"),
        )
        otp.delete()
        return True
    else:
        return False
