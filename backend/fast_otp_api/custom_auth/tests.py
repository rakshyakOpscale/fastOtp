import io

from django.test import TestCase
from django.conf import settings
from django.urls import reverse

from rest_framework.parsers import JSONParser

from .models import User

# Create your tests here.

verify_otp = [{"phone_number": "9772166609", "otp_code": "12345"}]


refresh = {
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY3NjM1NzQ0MywiaWF0IjoxNjc2MzU1NjQzLCJqdGkiOiIxNDlmMjc3YTkzMWQ0YTdkOTQ1YmRiODg5YjFhZGNjNCIsInVzZXJfaWQiOjF9.-0s-I-wprSNCM4MEClJphUslnHZCI_Y3jBeI-PhraIg",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjc2MzU3NDQzLCJpYXQiOjE2NzYzNTU2NDMsImp0aSI6ImFhZjQyNGQyNjUzZjRlZDliY2RjYTRlOWRiMTMxOTUyIiwidXNlcl9pZCI6MX0.e27RiEdY4WhmdSfxGjVqJXszdIjOea39Zsrc7BmLgBA",
}


class UserTest(TestCase):

    def test_sms_send_service(self):
        response = self.client.post(
            reverse("custom_auth:send_otp"), data={"phone_number": settings.TEST_PHONE}
        )
        self.assertEqual(response.status_code, 201)