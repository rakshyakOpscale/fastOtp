from django.shortcuts import render

from rest_framework.generics import RetrieveAPIView
from rest_framework.viewsets import ModelViewSet

from .models import Profile
from .serializers import ProfileSerializer

# Create your views here.


class ProfileView(RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
