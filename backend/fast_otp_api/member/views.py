from django.shortcuts import render
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateAPIView
from .models import Config, Contact, App
from .serializers import ConfigSerializer, ContactSerializer, AppSerializer

# Create your views here.


class ConfigView(ListAPIView):
    queryset = Config.objects.all()
    serializer_class = ConfigSerializer


class AppView(CreateAPIView):
    queryset = App.objects.all()
    serializer_class = AppSerializer


class AppViewUpdate(RetrieveUpdateAPIView):
    queryset = App.objects.all()
    serializer_class = AppSerializer


class ContactView(ListAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
