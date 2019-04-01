from rest_framework import permissions


class UsernamePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action == 'create':
            return True
        elif view.action == 'list' or view.action == 'destroy':
            return request.user.is_authenticated and request.user.is_admin
        elif view.action in ['retrieve', 'update', 'partial_update']:
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        if view.action in ['retrieve', 'update', 'partial_update']:
            return obj == request.user or request.user.is_admin
        if view.action == 'destroy':
            return request.user.is_admin
        else:
            return False

