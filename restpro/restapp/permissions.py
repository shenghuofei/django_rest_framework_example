# -*- encoding:utf-8 -*-
from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    自定义权限只允许对象的所有者编辑它。
    """
    print "owner has permission"
    def has_object_permission(self, request, view, obj):
        print "has permission"
        print request.user,obj.owner
        # 读取权限允许任何请求，
        # 所以我们总是允许GET，HEAD或OPTIONS请求。
        if request.method in permissions.SAFE_METHODS:
            return True

        # 只有该snippet的所有者才允许写权限。
        return obj.owner == request.user

class AllReadOnly(permissions.BasePermission):
    print "all can get"
    def has_object_permission(self, request, view, obj):
        return True
