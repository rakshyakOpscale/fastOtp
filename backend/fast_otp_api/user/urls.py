from django.urls import path

from .views import ProfileView

urlpatterns = [
    path(
        "profile/<pk>",
        ProfileView.as_view({"get": "retrieve", "patch": "partial_update"}),
        name="profile",
    ),
    path(
        "profile/",
        ProfileView.as_view({"get": "list"}),
        name="profile-list",
    ),
]
