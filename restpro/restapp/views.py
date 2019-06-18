# -*- coding:utf-8 -*-
from django.shortcuts import render

# Create your views here.
from django.core.signals import request_started, request_finished
from django.dispatch import receiver
import django.dispatch
from django.http import HttpResponse
from rest_framework import status,mixins,generics
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from restapp.models import Snippet
from restapp.seris import spsl
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from rest_framework import permissions
from restapp.permissions import IsOwnerOrReadOnly,AllReadOnly
from django.contrib.auth.decorators import login_required
import json,random


'''
自定义信号:
使用django.dispatch.Signal定义信号，使用Signal.send()发送信号
这段代码声明了request_done信号，它向接受者提供name和size参数
接受者my_signal_callback收到信号后，简单输出内容
'''
request_done = django.dispatch.Signal(providing_args=["name","size"])
@receiver(request_done)
def my_signal_callback(sender, **kwargs):
    print("this is my custom signal handler")
    print(sender,kwargs)

# 使用receiver装饰器连接信号
@receiver(request_finished)
def my_callback(sender, **kwargs):
    print("this is another Request finished handler!")

def request_started_handler(sender, **kwargs):
    print('start request')
    print('start kwargs',kwargs)
    print(dir(sender))

def request_finished_handler(sender, **kwargs):
    print('finish request')
    print('finish kwargs',kwargs)
    print(dir(sender))

@api_view(['GET','POST'])
def signal_test(request):
    # 使用connect连接信号接受者
    request_started.connect(request_started_handler)
    print('i am signal test')
    request_finished.connect(request_finished_handler)
    # 发送自定义信号
    request_done.send(sender=request, name="signal_test", size=123)
    return Response('ok')

@api_view(['GET','POST'])
def sp_list(request):
    print "request: ",dir(request)
    print "request data: ",request.data
    print "request user: ",request.user
    print "request auth: ",request.auth
    if request.method == 'GET':
        sp = Snippet.objects.all()
        sl = spsl(sp,many=True)
        print "sl dir: ",dir(sl)
        return Response(sl.data)
    elif request.method == 'POST':
        print "post data: ",request.data[0]
        owner = User.objects.first()
        pdata = request.data[0]
        pdata['owner'] = owner
        s = Snippet(**pdata)
        s.save()
        return Response(s)
        #return Response(status=200)

@api_view(['GET'])
def profile(request):
   print("users:", request.user)
   print("auth:", request.auth)
   print("request.authenticators:",request.authenticators)
   if request.user:
       return Response(request.user.username) 
   else:
       return Response("failed") 

class csp_list(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly,)  #通过身份验证的有读写权限，否则只有只读权限
    def get(self,request,format=None):
        sp = Snippet.objects.all()
        sl = spsl(sp,many=True)
        return Response(sl.data)
    def post(self,request,format=None):
        #owner = User.objects.first()
        pdata = request.data[0]
        #pdata['owner'] = owner
        s = spsl(data=pdata)
        if s.is_valid():
            s.save()
        #s = Snippet(**pdata)
        #s.save()
        return Response(s.data)

class getvalue(APIView):
    # permission_classes = (permissions.IsAuthenticated,AllReadOnly,)
    # 在view中指定特定的throttle classes
    from mythrottle import SpecUserThrottle 
    throttle_classes = (SpecUserThrottle,)
    def get(self,request,format=None):
        print("getvalue request:",request)
        print("getvalue request:",request.user)
        data = []
        for i in range(12):
            data.append(random.randint(0, 100)) # 0到100间的随机数 
        response = HttpResponse(json.dumps({'data':data,'errno':'0'}))
        response["Access-Control-Allow-Origin"] = "*"
        return response

'''
requests example:
headers = {'Authorization': 'Token f165baa8ee7d23f48289aed29579c25cbd8e3247'}
res = requests.get('http://localhost:9000/vue/',headers=headers)
'''
class vueget(APIView):
    def get(self,request,format=None):
        print "data: ",request.data
        print "body: ",request.body
        print "params: ",request.query_params
        print "params username: ",request.query_params.get('username')
        response = HttpResponse(json.dumps({'data':'ok','errno':'0'}))
        response["Access-Control-Allow-Origin"] = "*"
        return response
    def post(self,request,format=None):
        print "data: ",request.data
        print "date: ",json.loads(request.data.keys()[-1])['date']
        #print "body: ",request.body
        print "params: ",request.query_params
        response = HttpResponse(json.dumps({'data':'ok','errno':'0'}))
        response["Access-Control-Allow-Origin"] = "*"
        return response


#mixins
class msp_list(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly,)
    queryset = Snippet.objects.all()
    serializer_class = spsl 

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

#generics
class gsp_list(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly,)
    queryset = Snippet.objects.all()
    serializer_class = spsl


class gsp_detail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly,)
    queryset = Snippet.objects.all()
    serializer_class = spsl

# login_required 和rest_framework的登录验证同时只用一个就可以了
# login_required检查如果未登陆则会跳转到settings.LOGIN_URL
@login_required
def test_login_required(request):
    response = HttpResponse(json.dumps({'data':'ok','errno':'0'}))
    return response

'''
当服务启动就自动开始执行,在开发模式(runserver)下测试发现确实在启动是执行了
但是执行后,就无法响应其他的请求了，貌似阻止了Django的启动过程
'''
def my_init_run():
    import time
    while(True):
        print('when start to run')
        time.sleep(2)
# my_init_run()
