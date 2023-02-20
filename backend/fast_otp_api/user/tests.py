from django.test import TestCase
from django.conf import settings

from .models import Profile, User

# Create your tests here.


class ProfileModelTest(TestCase):
    def setUp(self) -> None:
        user = User.objects.create(phone_number=settings.TEST_PHONE)
        Profile.objects.create(user_id=user)

    def test_field_verbose_name(self):
        profile = Profile.objects.get(id=1)
        first_name = profile._meta.get_field("first_name").verbose_name
        last_name = profile._meta.get_field("last_name").verbose_name
        user_id = profile._meta.get_field("user_id").verbose_name
        self.assertEqual(first_name, "first name")
        self.assertEqual(last_name, "last name")
        self.assertEqual(user_id, "user id")

    def test_field_max_len(self):
        profile = Profile.objects.get(id=1)
        first_name_max_len = profile._meta.get_field("first_name").max_length
        last_name_max_len = profile._meta.get_field("last_name").max_length
        self.assertEqual(first_name_max_len, 120)
        self.assertEqual(last_name_max_len, 120)

    def test_obj_name(self):
        profile = Profile.objects.get(id=1)
        expected_name = f"{profile.user_id.phone_number}"
        self.assertEqual(str(profile), expected_name)
