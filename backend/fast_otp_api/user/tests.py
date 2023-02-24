import logging

from django.test import TestCase
from django.urls import reverse
from django.conf import settings

from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Profile, User

# Create your tests here.


class ProfileModelTest(TestCase):
    def setUp(self) -> None:
        user = User.objects.create(phone_number=settings.TEST_PHONE)
        Profile.objects.create(user=user)

    def test_obj_str_name(self):
        profile = Profile.objects.get(id=1)
        self.assertEqual(profile.__str__(), profile.user.phone_number)

    def test_field_verbose_name(self):
        profile = Profile.objects.get(id=1)
        first_name = profile._meta.get_field("first_name").verbose_name
        last_name = profile._meta.get_field("last_name").verbose_name
        user = profile._meta.get_field("user").verbose_name
        self.assertEqual(first_name, "first name")
        self.assertEqual(last_name, "last name")
        self.assertEqual(user, "user")

    def test_field_max_len(self):
        profile = Profile.objects.get(id=1)
        first_name_max_len = profile._meta.get_field("first_name").max_length
        last_name_max_len = profile._meta.get_field("last_name").max_length
        self.assertEqual(first_name_max_len, 120)
        self.assertEqual(last_name_max_len, 120)

    def test_obj_name(self):
        profile = Profile.objects.get(id=1)
        expected_name = f"{profile.user.phone_number}"
        self.assertEqual(str(profile), expected_name)


class APITest(TestCase):
    def setUp(self) -> None:
        import random

        self.user1 = str(random.randint(9999900000, 9999999999))
        self.user2 = str(random.randint(9999900000, 9999999999))
        logging.basicConfig(filename="test.log", level=logging.DEBUG)

        User.objects.create_user(phone_number=self.user1, password=str(self.user1))
        User.objects.create_user(phone_number=self.user2, password=str(self.user2))

        User.objects.create_superuser(
            phone_number=settings.TEST_PHONE, password=str(settings.TEST_PHONE)
        )
        self.user1 = User.objects.get(id=1)
        self.user2 = User.objects.get(id=2)
        self.superuser = User.objects.get(phone_number=settings.TEST_PHONE)
        self.profil = Profile.objects.create(user=self.user1)
        self.profil = Profile.objects.create(user=self.user2)
        self.profil = Profile.objects.create(user=self.superuser)

        self.user1AccessToken = str(RefreshToken().for_user(self.user1).access_token)
        self.user2AccessToken = str(RefreshToken().for_user(self.user2).access_token)
        self.superUserAccessToken = str(
            RefreshToken().for_user(self.superuser).access_token
        )

    def test_profile_get(self):

        response = self.client.get(
            reverse("user:profile"),
            HTTP_AUTHORIZATION="Bearer %s" % self.user2AccessToken,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(
            reverse("user:profile-detail", args=[self.user1.id]),  # type: ignore
            HTTP_AUTHORIZATION="Bearer %s " % self.user2AccessToken,
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_profile_get_all(self):

        self.client.login(
            phone_number=self.superuser.phone_number,
            password=str(self.superuser.phone_number),
        )

        response = self.client.get(
            reverse("user:profile"),
            HTTP_AUTHORIZATION="Bearer %s" % self.superUserAccessToken,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        import json

        data = json.loads(response.content.decode("utf-8"))
        self.assertEqual(type(data), list)
