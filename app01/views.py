import hashlib
from django.shortcuts import render,HttpResponse
from rest_framework.views import APIView  # 继承 apiview
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from app01 import models
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication
from rest_framework.authentication import BasicAuthentication
from rest_framework.authentication import BaseAuthentication
from rest_framework.permissions import AllowAny
# Create your views here.

# class MyAuthentication(object):
#     def authenticate(self,request):
#         token = request.query_params.get('token')
#         if token == 'ff':
#             return ('666','777')
#         raise APIException('sorry!')
#
#
# class Hostview(APIView):
#     authentication_classes = [MyAuthentication]   # 在 dispatch 里面调用
#     def get(self,request,*args,**kwargs):
#         print(request)
#         print(request.user)
#         print(request.auth)
#         return HttpResponse('..')

class AuthView(APIView):
    authentication_classes = []  # 不验证，因为是登录页面
    def get(self,request):
        print('111111111111')

        """
        使用 get 方法，接收用户名和密码
        :param request:
        :return:
        """
        ret = {'code':1000,'msg':None}
        user = request.query_params.get('user')
        pwd = request.query_params.get('pwd')
        obj = models.UserInfo.objects.filter(username=user,password=pwd).first()
        if not obj:
            ret['code'] = 1001
            ret['msg'] = 'username or password is error!!!'
            return Response(ret)
        # 创建随机字符串
        import time
        ctime = time.time()
        key = '%s|%s'%(user,ctime)
        # 加密
        m = hashlib.md5()
        m.update(key.encode('utf8'))
        token = m.hexdigest()
        # 保存数据
        obj.token = token
        obj.save()

        ret['token'] = token
        return Response(ret)



class MyAuthentication(BaseAuthentication):
        def authenticate(self,request):
            token = request.query_params.get('token')
            obj = models.UserInfo.objects.filter(token=token).first()
            if obj:
                return (obj.username,obj)
            return None  # 表示我不处理，留给下一个处理。


class MyPermission(object):
    message = '无权访问'
    def has_permission(self,request,view):
        if request.user:
            return True
        return False

class AdminPermission(object):
    message = 'admin_无权访问'
    def has_permission(self,request,view):
        if request.user == 'ff':
            return True
        return False

class HostView(APIView):
    """匿名用户和登录用户都可以访问"""
    authentication_classes = [MyAuthentication ,]
    permission_classes = []    # 不验证该 url
    def get(self,request,*args,**kwargs):
        # 原来的 request 对象：django.core.handlers.wsgi.WSGIRequest
        # 现在的 request 对象：rest_framework.request.Request
        self.dispatch(request)
        # print(request.user)
        # print(request.token)
        return Response('刘 gay 日华是狗🐶🐶🐶🐶🐶🐶')


class UserView(APIView):
    """仅限登录后的用户访问"""
    authentication_classes = [MyAuthentication]
    permission_classes = [MyPermission]
    def get(self,request,*args,**kwargs):
        return Response('用户列表')


class SalaryView(APIView):
    """
    只有admin用户才可以访问
    """
    authentication_classes = [MyAuthentication ,]
    permission_classes = [MyPermission ,AdminPermission ,]
    def get(self,request,*args,**kwargs):
        return Response('查看薪资列表，仅限 admin 用户')