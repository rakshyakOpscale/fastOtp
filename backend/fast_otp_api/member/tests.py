import logging

from django.test import TestCase
from django.conf import settings

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

    logging.basicConfig(
        filename="test.log",
        level=logging.DEBUG,
        format="ConfigModelTest:%(levelname)s:%(name)s:%(message)s",
    )

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
        self.assertEqual(app.get_absolute_url(), "/api/member/app/detail/1/")

    def test_obj_name(self):
        app = App.objects.get(id=1)
        expected_name = f"{app.display_name} {app.label}"
        self.assertEqual(str(app), expected_name)


class ContactModelTest(TestCase):
    def setUp(self) -> None:
        Contact.objects.create(
            phone_number=settings.TEST_PHONE,
            label="friend",
            first_name="Rahul",
            last_name="joshi",
        )

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
        App.objects.create(
            display_name="amazone",
            package_name="com.package.amazone",
            label="ecommarce",
        )
        Contact.objects.create(
            phone_number=settings.TEST_PHONE,
            label="brother",
            first_name="Rohit",
            last_name="Sharma",
        )
        User.objects.create(phone_number=settings.TEST_PHONE, is_verified=True)

        user = User.objects.get(id=1)
        app = App.objects.get(id=1)
        contact = Contact.objects.get(id=1)

        Profile.objects.create(user=user)
        profile = Profile.objects.get(id=1)

        Config.objects.create(profile=profile)

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
