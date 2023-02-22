from django.contrib.auth.models import AnonymousUser

from rest_framework import permissions


class UserOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser or request.user is AnonymousUser:
            return False
        else:
            return True


class SuperUserOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return True if request.user.is_superuser else False
