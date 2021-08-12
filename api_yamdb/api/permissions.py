from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsRoleAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and user.role == 'admin' or user.is_staff

    def has_object_permission(self, request, view, obj):
        user = request.user
        return user.is_authenticated and user.role == 'admin' or user.is_staff


class IsSuperUser(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_superuser


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return bool(request.user.is_staff or request.user.role == 'admin')
