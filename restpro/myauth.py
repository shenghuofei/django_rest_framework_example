#!/usr/bin/env python
#-*- coding:utf-8 -*-

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password

class MyBackend(object):
    """
    Authenticate against the settings ADMIN_LOGIN and ADMIN_PASSWORD.

    Use the login name, and a hash of the password. For example:

    ADMIN_LOGIN = 'admin'
    ADMIN_PASSWORD = 'sha1$4e987$afbcf42e21bd417fb71db8c66b321e9fc33051de'
    """

    def authenticate(self, username=None, password=None, sid=None):
        #login_valid = (settings.ADMIN_LOGIN == username)
        #pwd_valid = check_password(password, settings.ADMIN_PASSWORD)
        if not username:
            return None
        #if login_valid and pwd_valid:
        else:
            print(username,password,sid)
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                # Create a new user. Note that we can set password
                # to anything, because it won't be checked; the password
                # from settings.py will.
                user = User(username=username, password='123456')
                user.is_staff = True
                user.is_superuser = False
                user.save()
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

