from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model

from .models import User

UserModel = get_user_model()


class CustomBackend(BaseBackend):
    def authenticate(self, request, phone_number=None):
        if phone_number is None:
            raise TypeError("phoen got None, must be User.phone_number")
        try:
            user = User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            raise ValueError(f"can not find user with phone {phone_number}")
        return user

    def get_user(self, user_id: int):
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise ValueError(f"can not find user with user id {user_id}")
        return
