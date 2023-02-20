from django.urls import path

# relative path
from .views import (
    log_out_user,
    UsersViewSet,
    JwtTokenVerifyView,
    JwtTokenRefreshView,
    SendOtpViewSet,
    OtpVerifyViewSet,
)

app_name = "custom_auth"

urlpatterns = [
    path("users/", UsersViewSet.as_view({"get": "list"}), name="users"),
    path("send-otp/", SendOtpViewSet.as_view({"post": "create"}), name="send_otp"),
    path(
        "verify-otp/",
        OtpVerifyViewSet.as_view({"post": "create"}),
        name="verify_otp",
    ),
    path("login/", JwtTokenVerifyView.as_view(), name="login"),
    path("token/refresh/", JwtTokenRefreshView.as_view(), name="refresh_token"),
    path("logout/", log_out_user, name="logout"),
]
