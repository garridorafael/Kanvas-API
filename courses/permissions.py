from rest_framework import permissions
from rest_framework.permissions import BasePermission


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        if request.user.is_authenticated and request.method in permissions.SAFE_METHODS:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        if request.user.is_authenticated and request.method in permissions.SAFE_METHODS:
            return True

        if request.user.id and obj.students.filter(id=request.user.id).exists():
            return True

        return False


class IsAdminOrStudentCanAccessContent(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        return True

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        if obj.course.students.filter(id=request.user.id).exists():
            return True

        return False
