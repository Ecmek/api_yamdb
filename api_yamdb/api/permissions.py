from rest_framework import permissions


class IsRoleAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and user.role == 'admin' or user.is_staff

    def has_object_permission(self, request, view, obj):
        user = request.user
        return user.is_authenticated and user.role == 'admin' or user.is_staff


class IsRoleModerator(permissions.BasePermission):

    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and user.role == 'moderator'

    def has_object_permission(self, request, view, obj):
        user = request.user
        return user.is_authenticated and user.role == 'moderator'


class IsAuthorOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return (
            obj.author == request.user
            or request.method in permissions.SAFE_METHODS
        )


class ReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS
