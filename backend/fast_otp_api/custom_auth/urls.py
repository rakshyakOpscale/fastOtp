from django.urls import path

# relative path
from .views import verify_otp_create_user, send_otp, login_user, log_out_user, UsersViewSet

urlpatterns = [
    path("users/", UsersViewSet.as_view({"get": "list"}), name="users"),
    path("send-otp/", send_otp, name="send-otp"),
    path("verify-otp/", verify_otp_create_user, name="verify-otp-create-user"),
    path("login/<pk>",login_user, name="login"),
    path("logout/", log_out_user, name="logout"),
]
