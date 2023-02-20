import io

from django.test import TestCase
from django.conf import settings
from django.urls import reverse

from django.contrib.auth import authenticate
from django.db.utils import IntegrityError

from rest_framework.parsers import JSONParser

from .models import User

# Create your tests here.


class UserTest(TestCase):
    def setUp(self) -> None:
        User.objects.create_user(
            phone_number=settings.TEST_PHONE, password=settings.TEST_PHONE
        )

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
