from django.urls import path
from .views import (
    AppViewSet,
    ConfigViewSet,
    ContactViewSet,
    ConfigAddMoreAppViewSet,
    AppDetailViewSet,
    ConfigDetailViewset,
    ContactDetailViewSet,
)

urlpatterns = [
    path("config/", ConfigViewSet.as_view({"get": "list", "post": "create"})),
    path(
        "config/detail/<int:pk>/",
        ConfigDetailViewset.as_view(
            {"get": "retrieve", "patch": "partial_update", "delete": "destroy"}
        ),
    ),
    path("config/add-more/<pk>", ConfigAddMoreAppViewSet.as_view({"get": "retrieve", "patch": "partial_update"})),
    path("contact/", ContactViewSet.as_view({"get": "list", "post": "create"})),
    path(
        "contact/detail/<int:pk>/",
        ContactDetailViewSet.as_view(
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
        AppDetailViewSet.as_view(
            {"get": "retrieve", "patch": "partial_update", "delete": "destroy"}
        ),
    ),
]
