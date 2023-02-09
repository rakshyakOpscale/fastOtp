# main packages
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

# Create your models here.
class UserManager(BaseUserManager):
    def _create(self, phone_number, password, **extra):
        user = self.model(phone_number=phone_number, **extra)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phone_number, password, **extra):
        if not phone_number:
            raise ValueError("Users must have a phone_number field")

        extra.setdefault("is_superuser", True)
        extra.setdefault("is_staff", True)

        user = self._create(phone_number=phone_number, password=password, **extra)
        return user

    def create_user(self, phone_number, **extra):
        if not phone_number:
            raise ValueError("User must have a phone_number field")

        extra.setdefault("is_staff", True)
        user = self._create(phone_number=phone_number, password=None, **extra)
        return user


class BaseUser(AbstractBaseUser, PermissionsMixin):
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    # TODO:Add user permission

    class Meta:
        abstract = True


class User(BaseUser):
    phone_number = models.CharField(max_length=10, unique=True)
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = "phone_number"

    def __str__(self) -> str:
        return self.phone_number


class Otp(models.Model):
    otp_code = models.CharField(max_length=5)
    generated_time = models.TimeField(auto_now=True)
    expire_time = models.TimeField(blank=True, null=True)
    phone_number = models.CharField(max_length=10) 

    def __str__(self) -> str:
        return str(self.otp_code)