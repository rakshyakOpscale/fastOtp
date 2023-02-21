from django.contrib import admin
from .models import User, Otp

# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "phone_number", "is_staff", "is_verified", "is_superuser", "last_login")


admin.site.register(Otp)
