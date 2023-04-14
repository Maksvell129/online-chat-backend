from rest_framework import permissions


class IsMessageAuthor(permissions.BasePermission):
    """
    Custom permission to only allow the author of a message to delete or update it.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.author == request.user
