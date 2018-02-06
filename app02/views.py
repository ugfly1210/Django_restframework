from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.throttling import BaseThrottle,AnonRateThrottle,ScopedRateThrottle,SimpleRateThrottle,UserRateThrottle
from rest_framework.throttling import BaseThrottle,SimpleRateThrottle
from rest_framework.authentication import BaseAuthentication
from app01 import models
from rest_framework.renderers import JSONRenderer,BrowsableAPIRenderer

"""
要写权限相关，这是源码里面的，你需要重写这个方法
class BasePermission(object):

    def has_permission(self, request, view):
        return True
    def has_object_permission(self, request, view, obj):
        return True
"""



# class LimitView(APIView):
#     authentication_classes = []
#     permission_classes = []
#     self.dispatch
#     throttle_classes = []
#     def get(self,request,*args,**kwargs):
#         return  Response('控制访问品论')

class MyAuthentication(BaseAuthentication):
    """认证"""
    def authenticate(self, request):
        token = request.query_params.get('token')
        obj = models.UserInfo.objects.filter(token=token).first()
        if obj :
            return (obj.username,obj)
        return None
    def authenticate_header(self, request):
        pass

class MyPermission(object):
    message = '无权访问'
    def has_permission(self,request,view):
        print('ap02_view_34🎃===',view)
        if request.user:
            print('ap2_36_request',request)
            return True
        return False

class AdminPermission(object):
    message = '非 admin 用户无权访问'
    def has_permission(self,request,view):
        if request.user == 'ff':
            return True
        return False

class UserThrottle(SimpleRateThrottle):
    """对请求用户访问频率的限制"""
    scope = 'user_ff'  # 配置文件定义的显示频率的 key
    def get_cache_key(self, request, view):
        if request.user:
            return request.user
        # 如果是匿名用户的话，就不管啦
        return None


# 无需登录就可以访问
class AnonThrottle(SimpleRateThrottle):
    # 这个是配置文件定义的显示频率的 key
    # 在 settings 中获取anon_ff 对应的频率限制值
    scope = 'anon_ff'
    def get_cache_key(self, request, view):
        if request.user:
            return None
        return self.get_ident(request)



# 无需登录就可以访问
class IndexView(APIView):
    # 需要认证 MyAuthentication 然后，permission_classes 为空，即不需要权限相关操作。
    authentication_classes = [MyAuthentication ,]
    permission_classes = []
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    throttle_classes = [AnonThrottle,UserThrottle]

    def get(self,request,*args,**kwargs):
        self.dispatch
        return Response('欢迎来到首页')

# 需登录才可以访问
class ManageView(APIView):
    authentication_classes = [MyAuthentication]
    permission_classes = [MyPermission]
    throttle_classes = [AnonThrottle,UserThrottle]
    def get(self,request,*args,**kwargs):
        self.dispatch
        return Response('MangeView首页')