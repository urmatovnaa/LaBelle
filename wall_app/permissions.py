from rest_framework import permissions


class PostPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True
        else:
            if obj.owner == request.user:
                return True


class CommentPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # if request.method == 'Delete':
            # if
            # return True
        if request.method == 'PUT':
            if obj.owner == request.user:
                return True
