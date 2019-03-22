#!/usr/bin/env python
#-*- coding:utf-8 -*-

from django.contrib import auth
from django.contrib.auth import REDIRECT_FIELD_NAME, authenticate
from urllib2 import urlopen, Request
from django.shortcuts import redirect


def verify(request):
    if request.session.test_cookie_worked():
        request.session.delete_test_cookie()
    else:
        return False

    if request.user.is_authenticated():
        return True

    if request.method == 'POST':
        sid = request.POST.get('SID', '') or request.POST.get('sid', '')
        time = request.POST.get('time', '')
        sign = request.POST.get('sign', '')
    else:
        sid = request.GET.get('SID', '') or request.GET.get('sid', '')
        time = request.GET.get('time', '')
        sign = request.GET.get('sign', '')
    #username = 'from sso get username'
    req = Request(settings.SSO_API_URL + '/session/' + sid, headers=header)
    resp = urlopen(req)
    username = json.loads(resp.read())['data']['login']
    username = 'user1'
    # Using myauth.MyBackend
    user = authenticate(username=username, sid=sid)
    if user and user.is_active:
        request.session.set_expiry(0)
        auth.login(request, user)
        return True   
    return False

def login(request):
    session_key = 'sso_next'
    if verify(request):
        next_path = request.session.get(session_key, '/vue')
        if session_key in request.session:
            request.session.pop(session_key)
        return redirect(next_path)
    else:
        # Preserve the scene.
        if request.method == 'POST':
            next_path = request.POST.get(REDIRECT_FIELD_NAME, '/')
        else:
            next_path = request.GET.get(REDIRECT_FIELD_NAME, '/vue')
            print('logind',request.user.username)
        request.session[session_key] = next_path
        # Use a unique callback URL.
        current_path = request.path
        callback_url = request.build_absolute_uri(current_path)
        #url = settings.SSO_AUTH_URL + '?service=' + urlquote(callback_url)
        url = callback_url

        request.session.set_test_cookie()
        return redirect(url)

def logout(request):
    auth.logout(request)
    redirect_url = request.build_absolute_uri(reverse('sso'))
    url = settings.SSO_LOGOUT_URL + '?service=' + urlquote(redirect_url)
    request.session.set_test_cookie()
    return redirect(url)

