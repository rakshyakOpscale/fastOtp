from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from .models import App, Config, Contact

from user.models import Profile

# create serializers here
class AppSerializer(ModelSerializer):
    class Meta:
        model = App
        fields = ["id", "display_name", "label", "package_name"]


class ContactSerializer(ModelSerializer):
    class Meta:
        model = Contact
        fields = ["id", "phone_number", "label", "first_name", "last_name"]


class ConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = Config
        fields = "__all__"
