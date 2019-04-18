#-*- coding:utf-8 -*-
"""restpro URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf import settings 
from django.conf.urls import url
from django.contrib import admin
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls import include
from rest_framework.schemas import get_schema_view
from rest_framework.authtoken import views as restviews
from django.contrib.auth import views as auth_views
 
schema_view = get_schema_view(title='Pastebin API')

from restapp import views
from restapp import login
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^gentoken/', restviews.obtain_auth_token),
    url(r'^login/$', login.login, name='login'),
    url('^schema/$', schema_view),
    url('^accounts/profile/$', views.profile),
    url(r'^signal/$', views.signal_test),
    url(r'^list/$', views.sp_list),
    url(r'^sp/(?P<pk>[0-9]+)/$', views.sp_list),
    url(r'^clist/$', views.csp_list.as_view()),
    url(r'^csp/(?P<pk>[0-9]+)/$', views.csp_list.as_view()),
    url(r'^mlist/$', views.msp_list.as_view()),
    url(r'^msp/(?P<pk>[0-9]+)/$', views.msp_list.as_view()),
    url(r'^glist/$', views.gsp_list.as_view()),
    url(r'^gsp/(?P<pk>[0-9]+)/$', views.gsp_detail.as_view()),
    url(r'^vue/$', views.vueget.as_view()),
    url(r'^getvalue/$', views.getvalue.as_view()),
    url(r'^test/login/required$', views.test_login_required),
]

urlpatterns = format_suffix_patterns(urlpatterns)

# rest_framework login
urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

# 使用django 认证视图
urlpatterns += [
    url('^django/', include('django.contrib.auth.urls')),
    # 登出一个用户，然后重定向到登录页面,login_url 默认为settings.LOGIN_URL
    url('^django/logout/then/login', auth_views.logout_then_login)
]
