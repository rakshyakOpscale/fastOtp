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
    profile = models.ForeignKey(Profile, on_delete=models.PROTECT)
    choice = (("2h", "2 hours"), ("to", "today"), ("tm", "tomarrow"), ("al", "always"))
    contact = models.ManyToManyField(Contact)
    selected_apps = models.ManyToManyField(App)
    # share_otp_for = models.CharField()
    set_duration = models.CharField(max_length=2, choices=choice, default="2h")
    created_on = models.DateTimeField(auto_now=True)
    last_update = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return self.profile.user_id.phone_number


class OtpTimeline(models.Model):
    method = models.CharField(max_length=1, choices=(("1", "sent"), ("0", "receive")))
    contact = models.ForeignKey(Contact, on_delete=models.PROTECT)
    sent_date = models.DateTimeField(auto_now=True)
    update_data = models.DateTimeField(auto_now_add=True)
    provider = models.CharField(max_length=120)
