from rest_framework import permissions


class OnlySuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return True if request.user.is_superuser else False
