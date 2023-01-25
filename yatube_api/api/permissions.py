from rest_framework.permissions import BasePermission


class AuthorPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user != obj.author:
            return False
        return True
