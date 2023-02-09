from .models import Otp, User

import random
from django.http import HttpRequest


# ///////////////////interface////////////////////////////


class VerifyOtp(HttpRequest):
    phone_number: str
    otp_code: str


# ///////////////////methods////////////////////////////
def generte_otp(phone_number: str) -> str:
    """creates entry in the database and return otp_code"""
    instance = Otp.objects.create(
        phone_number=phone_number, otp_code=random.randint(10000, 99999)
    )
    instance.save()
    return instance.otp_code


def is_verified(data: VerifyOtp) -> bool:
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
        user: User = User.objects.get(phone_number=data.get("phone_number"))
        user.is_verified = True
        user.save()
        otp.delete()
        return True
    else:
        return False
