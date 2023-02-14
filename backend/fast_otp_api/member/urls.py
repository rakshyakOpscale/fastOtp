from django.urls import path
from .views import (
    AppViewSet,
    ConfigViewSet,
    ContactViewSet,
    ConfigAddMoreAppViewSet,
    OtpTimelineViewSet,
)

urlpatterns = [
    path("config/", ConfigViewSet.as_view({"get": "list", "post": "create"})),
    path(
        "config/detail/<int:pk>/",
        ConfigViewSet.as_view(
            {"get": "retrieve", "patch": "partial_update", "delete": "destroy"}
        ),
    ),
    path("config/add-more/<pk>", ConfigAddMoreAppViewSet.as_view({"get": "retrieve", "patch": "partial_update"})),
    path("contact/", ContactViewSet.as_view({"get": "list", "post": "create"})),
    path(
        "contact/detail/<int:pk>/",
        ContactViewSet.as_view(
            {"get": "retrieve", "patch": "partial_update", "delete": "destroy"}
        ),
    ),
    path(
        "app/",
        AppViewSet.as_view(
            {
                "get": "list",
                "post": "create",
            }
        ),
    ),
    path(
        "app/detail/<int:pk>/",
        AppViewSet.as_view(
            {"get": "retrieve", "patch": "partial_update", "delete": "destroy"}
        ),
    ),
     path(
        "otp-timeline/",
        OtpTimelineViewSet.as_view({"get": "list", "post": "create"}),
        name="otp-timeline",
    ),
     path(
        "otp-timeline/detail/<pk>",
        OtpTimelineViewSet.as_view({"get": "retrieve", "delete": "destroy"}),
        name="otp-timeline",
    ),
]
