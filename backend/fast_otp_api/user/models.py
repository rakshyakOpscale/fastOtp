from django.db import models

from custom_auth.models import User

# Create your models here.
class Profile(models.Model):
    first_name = models.CharField(max_length=120, blank=True)
    last_name = models.CharField(max_length=120, blank=True)
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.user_id.phone_number

