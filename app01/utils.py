from rest_framework.authentication import SessionAuthentication
from rest_framework.authentication import BasicAuthentication
from rest_framework.authentication import BaseAuthentication
from rest_framework.request import Request
from rest_framework.exceptions import APIException
from app01 import models



class MyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        print('2222222222')
        token = request.query_params.get('token')
        obj = models.UserInfo.objects.filter(token=token).first()
        print(token, obj.token)
        if obj:
            return (obj.username,obj)
            # Authenticate the request and return a two-tuple of (user, token).
        raise APIException('用户认证失败')
