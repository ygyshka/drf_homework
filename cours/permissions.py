from rest_framework.permissions import BasePermission


class IsOwnerOrStaff(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_staff:
            return True


class IsOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        if obj.user == request.user:
            return True


