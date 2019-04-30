#!/usr/bin/env python
#-*- coding:utf-8 -*-
from rest_framework.throttling import UserRateThrottle,BaseThrottle,SimpleRateThrottle

try:
    """
    Since Django 1.7 django.core.cache.caches is available, and replaces 
    django.core.cache.get_cache, which will be removed in Django 1.9. We 
    must ensure no use of get_cache is left.
    """
    from django.core.cache import get_cache
    get_cache_flag = True
except:
    from django.core.cache import caches
    get_cache_flag = False

VIP = ['wangfy']

######对匿名用户进行限流的类#####
class AnonThrottle(SimpleRateThrottle):
    scope = "obj_anon"   # 不同的scope可以设置不同的限流策略

    # cache = get_cache('throttling') if get_cache_flag else cache = caches['throttling']
    """
    如不是使用默认(default)的cache backend(settings中cache的配置),需要使用
    cache = get_cache($cache_name)或者cache = caches[$cache_name]来指定使用
    的cache backend,否则使用默认(default)的backend,django 1.9以后没有
    get_cache()函数，因此需要使用caches代替
    """

    # get_cache_key 返回用户唯一标示
    def get_cache_key(self, request, view):
        """
        Should return a unique cache-key which can be used for throttling.
        Must be overridden.

        May return `None` if the request should not be throttled. example:

        if not request.user:
            ident = self.get_ident(request)
        else:
            ident = request.user

        return self.cache_format % {
            'scope': self.scope,
            'ident': ident
        }
        """
        # 返回None，表示我不限制
        # 登录用户我不管
        if request.user:
            return None
        # 匿名用户
        # return self.get_ident(request)
        return self.cache_format % {
            'scope': self.scope,
            'ident': self.get_ident(request)
        }


######对登录用户进行限流的类#####
class UserThrottle(UserRateThrottle):
    scope = "obj_user" # 不同的scope可以设置不同的限流策略

    def get_cache_key(self, request, view):
        # 登录用户且不是VIP用户
        if request.user:
            if request.user.username not in VIP:
                return self.cache_format % {
                    'scope': self.scope,
                    'ident': request.user
                }
                # return request.user
        # 匿名用户和VIP用户我不管
        return None

######对VIP用户进行限流的类#####
class VIPUserThrottle(UserRateThrottle):
    scope = "obj_VIPuser"

    def get_cache_key(self, request, view):
        # VIP用户,如果VIP用户不限制的话，判断是VIP用户直接直接返回None即可,这里还是限制VIP用户的，只不过阈值较高
        if request.user:
            if request.user.username in VIP:#VIP用户
                return self.cache_format % {
                    'scope': self.scope,
                    'ident': request.user
                }
                # return request.user
        # 匿名用户和非VIP用户我不管
        return None
