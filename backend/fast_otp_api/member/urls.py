from django.urls import path
from .views import (
    AppView,
    AppViewUpdate,
    ConfigView,
    ConfigViewUpdate,
    ContactView,
    ContactViewUpdate,
)

urlpatterns = [
    path("config/", ConfigView.as_view()),
    path("config/update/<int:pk>/", ConfigViewUpdate.as_view()),
    path("contact/create/", ContactView.as_view()),
    path("contact/update/<int:pk>/", ContactViewUpdate.as_view()),
    path("app/create/", AppView.as_view()),
    path("app/update/<int:pk>/", AppViewUpdate.as_view()),
]
