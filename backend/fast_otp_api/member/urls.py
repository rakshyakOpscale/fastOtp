from django.urls import path
from .views import AppView, ConfigView, ContactView

urlpatterns = [path("member/config", ConfigView.as_view())]
