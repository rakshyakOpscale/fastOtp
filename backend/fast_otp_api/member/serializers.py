from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from .models import App, Config, Contact

# create serializers here
class AppSerializer(ModelSerializer):
    class Meta:
        model = App
        # fields = ["id", "display_name", "label", "package_name"]
        fields = "__all__"


class AppListSerializer(serializers.ListSerializer):
    child = AppSerializer()

    def create(self, validated_data):
        instance = [App(**attrs) for attrs in validated_data]
        return App.objects.bulk_create(instance)


class ContactSerializer(ModelSerializer):
    class Meta:
        model = Contact
        fields = ["id", "phone_number", "label", "first_name", "last_name"]


class ConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = Config
        fields = ["id", "set_duration", "profile_id", "contact", "selected_apps"]

    contact = ContactSerializer()
    selected_apps = AppListSerializer()
