from rest_framework import permissions

from accounts.models import User
from core.utils import exception


class IsNotAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        user: User = request.user
        if user is None or user.is_anonymous:
            return True
        raise exception.NotAllowAuthentication
