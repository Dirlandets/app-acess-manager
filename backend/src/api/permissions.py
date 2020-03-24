from rest_framework import permissions

from applications.models import Application


class TokenIsActivePermission(permissions.BasePermission):
    """
    Permission check for token is Valid.
    """
    def has_permission(self, request, view):
        token = request.headers.get('Token', None)
        active = Application.objects.filter(api_key=token).exists()
        return active
