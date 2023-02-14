from django.shortcuts import render
from rest_framework.generics import (
    RetrieveUpdateAPIView,
)
from rest_framework.viewsets import ModelViewSet

from .models import Config, Contact, App
from .serializers import (
    ConfigSerializer,
    ContactSerializer,
    AppSerializer,
    AppListSerializer,
)

# Create your views here.


class ConfigViewSet(ModelViewSet):
    queryset = Config.objects.all()
    serializer_class = ConfigSerializer


class ConfigDetailViewset(ModelViewSet):
    queryset = Config.objects.all()
    serializer_class = ConfigSerializer


class AppDetailViewSet(ModelViewSet):
    queryset = App.objects.all()
    serializer_class = AppSerializer


class AppViewSet(ModelViewSet):
    queryset = App.objects.all()
    serializer_class = AppSerializer
    list_serializer_class = AppListSerializer


class ContactDetailViewSet(ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer


class ContactViewSet(ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
