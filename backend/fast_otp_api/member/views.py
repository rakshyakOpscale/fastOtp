from django.shortcuts import get_object_or_404

from rest_framework.viewsets import ModelViewSet

from user.models import Profile

from .models import Config, Contact, App, OtpTimeline
from .permissions import SuperUserOnly
from .permissions import UserOnly
from .serializers import (
    ConfigAdminSerializer,
    ConfigUserSerializer,
    ConfigAddMoreAppSerializer,
    ContactSerializer,
    AppSerializer,
    AppListSerializer,
    OTPTimelineSerializer,
)

# Create your views here.


class ConfigViewSet(ModelViewSet):
    permission_classes = [UserOnly]

    def get_queryset(self):
        from user.models import Profile
        if not self.request.user.is_superuser:  # type: ignore
            profile = get_object_or_404(Profile, user=self.request.user)
            return Config.objects.filter(profile=profile)
        return Config.objects.all()

    def get_serializer_class(self):
        if self.request.user.is_superuser:  # type: ignore
            return ConfigAdminSerializer
        return ConfigUserSerializer


class ConfigAddMoreAppViewSet(ModelViewSet):
    queryset = Config.objects.all()
    serializer_class = ConfigAddMoreAppSerializer


class AppViewSet(ModelViewSet):
    permission_classes = [SuperUserOnly]
    queryset = App.objects.all()
    serializer_class = AppSerializer
    list_serializer_class = AppListSerializer


class ContactViewSet(ModelViewSet):
    permission_classes = [UserOnly]
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

    def get_queryset(self):
        profile = Profile.objects.get(user=self.request.user)
        return Contact.objects.filter(profile=profile)


class OtpTimelineViewSet(ModelViewSet):
    queryset = OtpTimeline.objects.all()
    serializer_class = OTPTimelineSerializer
