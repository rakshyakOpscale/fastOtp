from rest_framework import serializers

from .models import Profile
from member.serializers import ConfigSerializer

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            "id",
            "first_name",
            "last_name",
            "user_id",
        ]
    # user_id = serializers.StringRelatedField()
    user_id = serializers.StringRelatedField()
