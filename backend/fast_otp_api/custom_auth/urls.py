from django.urls import path

# relative path
from .views import UserGenericView, verify_otp_create_user, send_otp

urlpatterns = [
    path("profile/<int:pk>", UserGenericView.as_view(), name="users-list"),
    path("send-otp/", send_otp, name="send-otp"),
    path("verify-otp/", verify_otp_create_user, name="verify-otp-create-user"),
]
