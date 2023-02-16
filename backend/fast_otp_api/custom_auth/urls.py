from django.urls import path

# relative path
from .views import (
    verify_otp_create_user,
    send_otp,
    login_user,
    log_out_user,
    UsersViewSet,
    JwtTokenVerifyView,
    SendOtpViewSet,
    OtpVerifyViewSet,
)

urlpatterns = [
    path("users/", UsersViewSet.as_view({"get": "list"}), name="users"),
    path("send-otp/", SendOtpViewSet.as_view({"post": "create"}), name="send-otp"),
    path(
        "verify-otp/",
        OtpVerifyViewSet.as_view({"post": "create"}),
        name="verify-otp-create-user",
    ),
    path("login/", JwtTokenVerifyView.as_view(), name="login"),
    path("logout/", log_out_user, name="logout"),
]
