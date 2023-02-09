from django.db import models

# Create your models here.


class App(models.Model):
    display_name = models.CharField(max_length=120)
    package_name = models.CharField(max_length=260)
    label = models.CharField(max_length=120)


class Contact(models.Model):
    phone_number = models.CharField(max_length=10)
    label = models.CharField(max_length=120, default="family")
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)


class Config(models.Model):
    choice = (("2h", "2 hours"), ("to", "today"), ("tm", "tomarrow"), ("al", "always"))
    contact = models.OneToOneField(Contact, on_delete=models.CASCADE)
    selected_apps = models.ManyToManyField(App)
    # share_otp_for = models.CharField()
    set_duration = models.CharField(max_length=2, choices=choice, default="2h")
