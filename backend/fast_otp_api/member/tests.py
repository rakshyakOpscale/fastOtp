from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import authenticate
from django.db.utils import IntegrityError

from .models import Config, Contact, App, Profile

from custom_auth.models import User

# Create your tests here.


class MemberTest(TestCase):
    def setUp(self) -> None:
        for user in ["1234567891", "1234567892", "1234567893", "1234567894"]:
            User.objects.create_user(user, password=user).save()

        for app in ["amazone", "flipkart", "snapdeal"]:
            App.objects.create(
                display_name=app, package_name=f"com.package.{app}"
            ).save()

        for contact in ["1234567890", "1234567891", "1234567892"]:
            Contact.objects.create(
                phone_number=contact,
                first_name="rahul",
                last_name="sharma",
                label="ecommarce",
            ).save()

        for user in [user for user in User.objects.all()]:
            Profile.objects.create(user_id=user)

    def test_user_model(self):
        obj = User.objects.get(phone_number=1234567891)
        self.assertIsInstance(obj, User)
        self.assertEqual(obj.phone_number, str(1234567891))

        response = self.client.get(reverse("custom_auth:users"))
        self.assertEqual(response.status_code, 401)

        response = self.client.get(
            reverse("custom_auth:users"), HTTP_AUTHORIZATION="Bearer abc"
        )
        self.assertEqual(response.status_code, 401)

    def test_user_authentication(self):
        obj = authenticate(
            phone_number=1234567891,
            password="1234567891",
            backend="django.contrib.auth.backends.ModelBackend",
        )
        self.assertTrue(obj)

    def test_profile_model(self):
        profile = Profile.objects.all()
        self.assertGreater(len(profile), 0)