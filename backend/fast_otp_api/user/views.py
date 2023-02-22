from django.shortcuts import render

from rest_framework import viewsets

from .models import Profile
from .serializers import ProfileSerializer

# Create your views here.


class ProfileView(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def get_queryset(self):
        query = Profile.objects.filter(user=self.request.user)
        return query if not self.request.user.is_superuser else Profile.objects.all()  # type: ignore
