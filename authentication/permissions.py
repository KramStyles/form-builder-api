from rest_framework.permissions import BasePermission, IsAuthenticated

from .models import User


class FormBuilderPermissions(BasePermission):
    # This permission lets the user create and edit forms
    def has_permission(self, request, view):
        # This prevents a normal user from creating a form
        return not bool(request.user.user_type == 'normal')

    def has_object_permission(self, request, view, obj):
        allow = False
        try:
            # Allows admin or owner of the object to make changes
            if request.user.user_type == 'admin':
                allow = True
            else:
                owner = obj.author
                allow = bool(request.user == owner)
        except AttributeError:
            allow = False
        finally:
            return allow


class AdminPermissions(BasePermission):
    # This permission is for the admin which let's the user create both forms and fields
    def has_permission(self, request, view):
        # This allows only admins to perform a function like creating elements
        return bool(request.user.user_type == 'admin')

    def has_object_permission(self, request, view, obj):
        return True
