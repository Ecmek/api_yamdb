from rest_framework import permissions


class IsRoleAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and user.role == 'admin'

    def has_object_permission(self, request, view, obj):
        user = request.user
        return user.is_authenticated and user.role == 'admin'
