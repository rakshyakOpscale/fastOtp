import json
import logging

from django.test import TestCase
from django.conf import settings
from django.urls import reverse

from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from custom_auth.models import User

from .models import Config, Contact, App, Profile

# Create your tests here.


class AppModelTest(TestCase):
    def setUp(self) -> None:
        App.objects.create(
            display_name="amazone",
            package_name="com.package.amazone",
            label="ecommarce",
        )

    def test_obj_str_name(self):
        app = App.objects.get(id=1)
        self.assertEqual(app.__str__(), f"{app.display_name} {app.label}")

    def test_field_varbose_name(self):
        app = App.objects.get(id=1)
        display_name = app._meta.get_field("display_name").verbose_name
        package_name = app._meta.get_field("package_name").verbose_name
        label = app._meta.get_field("label").verbose_name

        self.assertEqual(display_name, "display name")
        self.assertEqual(package_name, "package name")
        self.assertEqual(label, "label")

    def test_field_max_length(self):
        app = App.objects.get(id=1)
        display_name_max_length = app._meta.get_field("display_name").max_length
        package_name_max_length = app._meta.get_field("package_name").max_length
        label_max_length = app._meta.get_field("label").max_length
        self.assertEqual(display_name_max_length, 120)
        self.assertEqual(package_name_max_length, 260)
        self.assertEqual(label_max_length, 120)

    def test_model_methods(self):
        app = App.objects.get(id=1)
        self.assertEqual(app.get_absolute_url(), "/api/member/app-detail/1/")

    def test_obj_name(self):
        app = App.objects.get(id=1)
        expected_name = f"{app.display_name} {app.label}"
        self.assertEqual(str(app), expected_name)


class ContactModelTest(TestCase):
    def setUp(self) -> None:
        user = User.objects.create(
            phone_number=settings.TEST_PHONE, password=settings.TEST_PHONE
        )
        Profile.objects.create(user=user, first_name="user", last_name="test")
        profile = Profile.objects.get(id=1)

        Contact.objects.create(
            profile=profile,
            phone_number=settings.TEST_PHONE,
            label="friend",
            first_name="Rahul",
            last_name="joshi",
        )

    def test_obj_str_name(self):
        contact = Contact.objects.get(id=1)
        self.assertEqual(contact.__str__(), f"{contact.first_name} {contact.last_name}")
    
    def test_model_methods(self):
        contact = Contact.objects.get(id=1)
        self.assertEqual(contact.get_absolute_url(), "/api/member/contact-detail/1/")

    def test_field_verbose_name(self):
        contact = Contact.objects.get(id=1)
        phone_number = contact._meta.get_field("phone_number").verbose_name
        label = contact._meta.get_field("label").verbose_name
        first_name = contact._meta.get_field("first_name").verbose_name
        last_name = contact._meta.get_field("last_name").verbose_name

        self.assertEqual(phone_number, "phone number")
        self.assertEqual(label, "label")
        self.assertEqual(first_name, "first name")
        self.assertEqual(last_name, "last name")

    def test_field_max_length(self):
        contact = Contact.objects.get(id=1)
        phone_number_max_len = contact._meta.get_field("phone_number").max_length
        label_max_len = contact._meta.get_field("label").max_length
        first_name_max_len = contact._meta.get_field("first_name").max_length
        last_name_max_len = contact._meta.get_field("last_name").max_length

        self.assertEqual(phone_number_max_len, 10)
        self.assertEqual(label_max_len, 120)
        self.assertEqual(first_name_max_len, 120)
        self.assertEqual(last_name_max_len, 120)


class ConfigModelTest(TestCase):
    def setUp(self) -> None:
        app = App.objects.create(
            display_name="amazone",
            package_name="com.package.amazone",
            label="ecommarce",
        )
        user = User.objects.create(
            phone_number=settings.TEST_PHONE, password=settings.TEST_PHONE
        )
        profile = Profile.objects.create(user=user)

        Config.objects.create(profile=profile, set_duration="2h")

    def test_obj_str_name(self):
        config = Config.objects.get(id=1)
        self.assertEqual(config.__str__(), f"{config.profile.user.phone_number}")

    def test_field_verbose_name(self):
        config = Config.objects.get(id=1)

        profile = config._meta.get_field("profile").verbose_name
        contact = config._meta.get_field("contact").verbose_name
        selected_apps = config._meta.get_field("selected_apps").verbose_name
        set_duration = config._meta.get_field("set_duration").verbose_name
        created_on = config._meta.get_field("created_on").verbose_name
        last_update = config._meta.get_field("last_update").verbose_name

        self.assertEqual(profile, "profile")
        self.assertEqual(contact, "contact")
        self.assertEqual(selected_apps, "selected apps")
        self.assertEqual(set_duration, "set duration")
        self.assertEqual(created_on, "created on")
        self.assertEqual(last_update, "last update")


class APITest(TestCase):
    def setUp(self) -> None:
        import random

        logging.basicConfig(filename="test.log", level=logging.INFO)

        RANDOME_USER_PHONE_NUMBER = random.randint(9970000000, 9999999999)

        self.userPhone = str(RANDOME_USER_PHONE_NUMBER)
        self.superuser = str(settings.TEST_PHONE)

        # create user
        User.objects.create_user(phone_number=self.userPhone, password=self.userPhone)
        User.objects.create_superuser(
            phone_number=self.superuser, password=self.superuser
        )

        logging.debug("Creating superuser and user.....")

        # get instance user and superuser
        self.user = User.objects.get(phone_number=self.userPhone)
        self.superuser = User.objects.get(phone_number=self.superuser)

        Profile.objects.create(user=self.user)
        self.userProfile = Profile.objects.get(user=self.user)

        logging.info(
            {
                "user": self.user,
                "superuser": self.superuser,
                "profile": self.userProfile,
            }
        )
        # generate access token
        self.userAccessToken = str(RefreshToken().for_user(self.user).access_token)
        self.superUserAccessToken = str(
            RefreshToken().for_user(self.superuser).access_token
        )
        logging.debug(
            {
                "userAccessToken": self.userAccessToken,
                "superusreAccessToken": self.superUserAccessToken,
            }
        )
        # create config
        Config.objects.create(profile=self.userProfile, set_duration="tm")

    def test_config_get_list_user_allowed(self):
        response = self.client.get(
            reverse("member:config"),
            HTTP_AUTHORIZATION="Bearer %s" % self.userAccessToken,
        )
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, "contact")

    def test_config_create(self):
        data = {}
        response = self.client.post(reverse("member:config"))

    def test_config_get_list_superuser_not_allowed(self):
        response = self.client.get(
            reverse("member:config"),
            HTTP_AUTHORIZATION="Bearer %s" % self.superUserAccessToken,
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_app_get_user_not_allowed(self):
        response = self.client.get(
            reverse("member:app"),
            HTTP_AUTHORIZATION="Bearer %s" % self.userAccessToken,
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.get(
            reverse("member:app-detail", args=[1]),
            HTTP_AUTHORIZATION="Bearer %s" % self.userAccessToken,
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_app_get_superuser_allowed(self):
        response = self.client.get(
            reverse("member:app"),
            HTTP_AUTHORIZATION="Bearer %s" % self.superUserAccessToken,
        )
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        app_data = {
            "display_name": "amazone",
            "package_name": "com.package.amazone",
            "label": "ecommarce",
        }
        App.objects.create(**app_data)
        response = self.client.get(
            reverse("member:app-detail", args=[1]),
            HTTP_AUTHORIZATION="Bearer %s" % self.superUserAccessToken,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_contact_superuser_not_allowed(self):
        response = self.client.get(
            reverse("member:contact"),
            HTTP_AUTHORIZATION="Bearer %s" % self.superUserAccessToken,
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_contact_user_allowed(self):
        Contact.objects.create(
            profile=self.userProfile,
            phone_number=self.userPhone,
            first_name="test",
            last_name="user",
        )

        resposne = self.client.get(
            reverse("member:contact"),
            HTTP_AUTHORIZATION="Bearer %s" % self.userAccessToken,
        )

        self.assertNotEqual(resposne.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(resposne.status_code, status.HTTP_200_OK)

        self.client.force_login(self.user)

        response = self.client.get(reverse("member:contact-detail", args=[1]))

        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
