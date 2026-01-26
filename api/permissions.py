"""
Custom permissions for ChargeNow API.
"""
from rest_framework.permissions import BasePermission
from django.contrib.auth.models import AnonymousUser


class IsUser(BasePermission):
    """Allow access only to regular users (role=1)"""

    def has_permission(self, request, view):
        user = request.user
        if not user or isinstance(user, AnonymousUser):
            return False

        return user.get('role') == 1


class IsOperator(BasePermission):
    """Allow access only to van operators (role=2)"""

    def has_permission(self, request, view):
        user = request.user
        if not user or isinstance(user, AnonymousUser):
            return False

        return user.get('role') == 2


class IsAdmin(BasePermission):
    """
    Allow access only to Django admin (superuser).
    No role-based admin.
    """

    def has_permission(self, request, view):
        user = request.user
        return hasattr(user, 'is_superuser') and user.is_superuser


class IsAdminOrOperator(BasePermission):
    """Allow access to Django admin or operator"""

    def has_permission(self, request, view):
        user = request.user

        if hasattr(user, 'is_superuser') and user.is_superuser:
            return True

        if not user or isinstance(user, AnonymousUser):
            return False

        return user.get('role') == 2
