from rest_framework.permissions import BasePermission


class IsStaff(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        return False


class IsOwner(BasePermission):

    def has_object_permission(self, request, view, obj):

        if obj.user == request.user:
            return True
        return False
