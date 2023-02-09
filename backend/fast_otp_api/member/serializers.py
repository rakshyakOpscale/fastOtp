from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import App, Config, Contact

# create serializers here
class AppSerializer(ModelSerializer):
    class Meta:
        model = App
        fields = ["display_name", "label"]


class ConfigSerializer(ModelSerializer):
    class Meta:
        model = Config
        fields = ["contact", "selected_apps", "set_duration"]


class ContactSerializer(ModelSerializer):
    class Meta:
        model = Contact
        fields = ["phone_number", "label", "first_name", "last_name"]
