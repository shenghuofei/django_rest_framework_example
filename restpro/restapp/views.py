# -*- coding:utf-8 -*-
from django.shortcuts import render

# Create your views here.
from django.core.signals import request_started, request_finished
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
from restapp.permissions import IsOwnerOrReadOnly
import json,random

def request_started_handler(sender, **kwargs):
    print('start request')
    print(dir(sender))

def request_finished_handler(sender, **kwargs):
    print('finish request')
    print(dir(sender))

@api_view(['GET','POST'])
def signal_test(requsts):
    request_started.connect(request_started_handler)
    print('i am signal test')
    request_finished.connect(request_finished_handler)
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
   print(request.user)
   print(request.auth)
   print(request.authenticators)
   return Response(request.GET) 

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
    def get(self,request,format=None):
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
