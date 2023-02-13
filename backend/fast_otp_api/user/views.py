from django.shortcuts import render

from rest_framework.generics import RetrieveAPIView

from .models import Profile
from .serializers import ProfileSerializer

# Create your views here.


class ProfileView(RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
