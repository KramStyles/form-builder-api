from rest_framework.permissions import BasePermission

from .models import User


class FormBuilderPermissions(BasePermission):
    # This permission lets the user create and edit forms
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        return True


class AdminPermissions(BasePermission):
    # This permission is for the admin which let's the user create both forms and fields
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        return True
