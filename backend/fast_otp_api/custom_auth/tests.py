import logging

from django.test import TestCase
from django.urls import reverse
from django.conf import settings
from django.contrib.auth import authenticate

from rest_framework_simplejwt.tokens import RefreshToken

from .models import User

# Create your tests here.


class UserTest(TestCase):
    def setUp(self) -> None:
        User.objects.create_user(
            phone_number=settings.TEST_PHONE, password=settings.TEST_PHONE
        )

    def test_obj_str_name(self):
        user = User.objects.get(id=1)
        self.assertEqual(user.__str__(), user.phone_number)

    def test_field_verbose_name(self):
        user = User.objects.get(id=1)
        phone_number = user._meta.get_field("phone_number").verbose_name
        is_verified = user._meta.get_field("is_verified").verbose_name

        self.assertEqual(phone_number, "phone number")
        self.assertEqual(is_verified, "is verified")

    def test_field_max_length(self):
        user = User.objects.get(id=1)
        phone_number_max_len = user._meta.get_field("phone_number").max_length

        self.assertEqual(phone_number_max_len, 10)

    def test_user_authentication(self):
        user = authenticate(
            phone_number=settings.TEST_PHONE, password=settings.TEST_PHONE
        )
        self.assertTrue(user.is_authenticated)  # type: ignore

    def test_failed_user_authentication(self):
        import random

        RANDOM_PHONE_NUMBER = random.randint(9970000000, 9999999999)
        user = authenticate(
            phone_number=RANDOM_PHONE_NUMBER, passowrd=str(RANDOM_PHONE_NUMBER)
        )
        self.assertEqual(user, None)


class APITest(TestCase):
    def setUp(self) -> None:

        import random

        logging.basicConfig(filename="test.log", level=logging.DEBUG)
        RANDOM_PHONE_NUMBER = random.randint(9970000000, 9999999999)

        self.user: str = str(RANDOM_PHONE_NUMBER)
        self.superuser: str = str(settings.TEST_PHONE)

        User.objects.create_user(phone_number=self.user, password=self.user)

        User.objects.create_superuser(
            phone_number=self.superuser, password=self.superuser
        )

        user = User.objects.get(phone_number=self.user)
        refresh = RefreshToken().for_user(user)

        self.userAccessToken: str = str(refresh.access_token)
        self.userRefreshToken: str = str(refresh)

        super_user = User.objects.get(phone_number=self.superuser)
        refresh = RefreshToken().for_user(super_user)

        self.superUserAccessToken: str = str(refresh.access_token)
        self.superUserRefreshToken: str = str(refresh)

    def test_users_without_authorization_header(self):
        response = self.client.get(reverse("custom_auth:users"))
        self.assertEqual(response.status_code, 403)
        logging.info(response.content)

    def test_user_authorization_get_users(self):
        response = self.client.get(
            reverse("custom_auth:users"),
            HTTP_AUTHORIZATION="Bearer %s" % self.userAccessToken,
        )
        self.assertEqual(
            response.content,
            b'{"detail":"You do not have permission to perform this action."}',
        )

    def test_superuser_authorization_get_users(self):
        response = self.client.get(
            reverse("custom_auth:users"),
            HTTP_AUTHORIZATION="Bearer %s" % self.superUserAccessToken,
        )
        self.assertEqual(response.status_code, 200)

    def test_user_login(self):
        response = self.client.post(
            reverse("custom_auth:login"), data={"token": self.userAccessToken}
        )
        self.assertContains(response, "token")

    def test_token_refresh(self):
        response = self.client.post(
            reverse("custom_auth:refresh_token"),
            data={"refresh": self.userRefreshToken},
        )
        self.assertContains(response, "access")
