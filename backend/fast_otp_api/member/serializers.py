from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import App, Config, Contact

# create serializers here
class AppSerializer(ModelSerializer):
    class Meta:
        model = App
        fields = ["display_name", "label", "package_name"]


class ContactSerializer(ModelSerializer):
    class Meta:
        model = Contact
        fields = ["phone_number", "label", "first_name", "last_name"]


class ConfigSerializer(serializers.Serializer):
    contact = serializers.StringRelatedField()
    selected_apps = AppSerializer(many=True)
    set_duration = serializers.TimeField()
