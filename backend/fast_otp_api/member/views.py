from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet

from .models import Config, Contact, App, OtpTimeline
from .serializers import (
    ConfigSerializer,
    ConfigAddMoreAppSerializer,
    ContactSerializer,
    AppSerializer,
    AppListSerializer,
    OTPTimelineSerializer,
)

# Create your views here.


class ConfigViewSet(ModelViewSet):
    queryset = Config.objects.all()
    serializer_class = ConfigSerializer

class ConfigAddMoreAppViewSet(ModelViewSet):
    queryset = Config.objects.all()
    serializer_class = ConfigAddMoreAppSerializer

class AppViewSet(ModelViewSet):
    queryset = App.objects.all()
    serializer_class = AppSerializer
    list_serializer_class = AppListSerializer

class ContactViewSet(ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer


class OtpTimelineViewSet(ModelViewSet):
    queryset = OtpTimeline.objects.all()
    serializer_class = OTPTimelineSerializer