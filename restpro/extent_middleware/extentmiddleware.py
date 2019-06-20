# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

'''
实现方法:
1.在项目目录下创建中间件目录extent_middleware(可自定义名字)并在下面创建__init__.py
2.在extent_middleware新增中间件文件extentmiddleware.py(可自定义名字)
3.实现中间件类(1.10.X以后可以是方法)extentmiddleware,并根据需要实现方法process_request，process_response，process_view等
4.在settings文件的MIDDLEWARE_CLASSES中增加自己的中间件extent_middleware.extentmiddleware.extentmiddleware(path.file.class)
'''

# 兼容新旧版本的django
try:
    from django.utils.deprecation import MiddlewareMixin  # Django 1.10.x
except ImportError:
    MiddlewareMixin = object  # Django 1.4.x - Django 1.9.x 
from django.shortcuts import redirect
from django.conf import settings
import time

class extentmiddleware(MiddlewareMixin):
    def process_request(self, request):
        print('before request')
        # 记录请求开始的时间，用于计算响应时间
        request._my_middle_start = time.time()
        # 可以在此检查是否登陆，未登陆则跳转至登陆页
        # return redirect(settings.LOGIN_URL)
 
    def process_response(self, request, response):
        print('after request')
        # 处理完成时间减去请求开始时间即响应时间
        if hasattr(request, '_my_middle_start'):
            print('request time:', time.time()-request._my_middle_start)
        return response

