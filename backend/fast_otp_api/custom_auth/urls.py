from django.urls import path

# relative path
from .views import UserGenericView, verify_otp, send_otp

urlpatterns = [
    path("", UserGenericView.as_view(), name="users-list"),
    path("send-otp", send_otp, name="send-otp"),
    path("verify-otp", verify_otp, name="verify-otp"),
]
