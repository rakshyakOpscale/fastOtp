from django.urls import path
from .views import AppView, AppViewUpdate, ConfigView, ContactView

urlpatterns = [
    path("member/config", ConfigView.as_view()),
    path("app/create", AppView.as_view()),
    path("app/update/<int:pk>", AppViewUpdate.as_view()),
]
