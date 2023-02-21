from rest_framework import permissions
from . import models


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)


class IsAdminOrCurrentProfile(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        profile = models.Profile.objects.get(user_id=user.id)
        post = models.Post.objects.filter(profile_id=profile.id)
        return bool(request.user and post or request.user.is_staff)