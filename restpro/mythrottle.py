#!/usr/bin/env python
#-*- coding:utf-8 -*-
from rest_framework.throttling import UserRateThrottle,BaseThrottle,SimpleRateThrottle

VIP = ['wangfy']

######对匿名用户进行限流的类#####
class AnonThrottle(SimpleRateThrottle):
    scope = "obj_anon"

    def get_cache_key(self, request, view):
        # 返回None，表示我不限制
        # 登录用户我不管
        if request.user:
            return None
        # 匿名用户
        return self.get_ident(request)

######对登录用户进行限流的类#####
class UserThrottle(SimpleRateThrottle):
    scope = "obj_user"

    def get_cache_key(self, request, view):
        # 登录用户且不是VIP用户
        if request.user:
            if request.user.username not in VIP:
                return request.user
        # 匿名用户和VIP用户我不管
        return None

######对VIP用户进行限流的类#####
class VIPUserThrottle(SimpleRateThrottle):
    scope = "obj_VIPuser"

    def get_cache_key(self, request, view):
        # VIP用户
        if request.user:
            if request.user.username in VIP:#VIP用户
                return request.user
        # 匿名用户和非VIP用户我不管
        return None
