from django.urls import path

from .views import ProfileView

app_name = "user"

urlpatterns = [
    path(
        "profile/",
        ProfileView.as_view({"get": "list"}),
        name="profile",
    ),
    path(
        "profile-detail/<pk>",
        ProfileView.as_view({"get": "retrieve", "patch": "partial_update"}),
        name="profile-detail",
    ),
]
