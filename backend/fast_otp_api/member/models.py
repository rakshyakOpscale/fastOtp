from django.db import models

from user.models import Profile

# Create your models here.


class App(models.Model):
    display_name = models.CharField(max_length=120)
    package_name = models.CharField(max_length=260, unique=True)
    label = models.CharField(max_length=120)

    def __str__(self) -> str:
        return f"{self.display_name} {self.label}"


class Contact(models.Model):
    phone_number = models.CharField(max_length=10, unique=True)
    label = models.CharField(max_length=120, default="family")
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"


class Config(models.Model):
    profile_id = models.ForeignKey(Profile, on_delete=models.PROTECT)
    choice = (("2h", "2 hours"), ("to", "today"), ("tm", "tomarrow"), ("al", "always"))
    contact = models.OneToOneField(Contact, on_delete=models.PROTECT, unique=True)
    selected_apps = models.ManyToManyField(App)
    # share_otp_for = models.CharField()
    set_duration = models.CharField(max_length=2, choices=choice, default="2h")
    created_on = models.DateTimeField(auto_now=True)
    last_update = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return self.profile_id.user_id.phone_number
