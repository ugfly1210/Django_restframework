# 二月五日note

### 课前：
  1. Low比三人组要自己可以写出来
  2. 设计模式了解
  

## 一：RESTful API
  - api：接口。
    - http://www.fff.com/get_users/
    - 上面的url就可以看做是接口。
    - 用途：
      - 一： 为别人提供服务
      - 二： 前后端分离
  - restful：表征状态转移、面向资源编程
    - 面向资源：对互联网上的任意东西都视为资源。
      - 再理解：每一个url对应的数据就是资源。

补充：restful不是协议，是规定。协议是指http那类。

**之前的api写法：**
http://www.ugfly.com/get_girls/
http://www.ugfly.com/add_girl/
http://www.ugfly.com/del_girl/1/
http://www.ugfly.com/update_girl/1/

**restful api**
http://www.ugfly.com/girls/
GET：获取
POST：添加
PUT：更新
DELETE：删除
## restful 设计规则 即规范：
```
## 1. 对于restful，要在域名加以区分。加api
## 2. 版本:v1,v2,v3
## 3. 路径，要使用名词（可复数）
  https://api.example.com/v1/zoos
  https://api.example.com/v1/animals
  https://api.example.com/v1/employees
## 4. 状态码
## 5. 错误处理。当状态码为4xx时，应该返回错误信息，error应当做key。
## 6. 根据 method 不同，表示增删改查。
## 7. 超链接 Hypermedia link
############## 总结：以上都是参考，具体情况请具体分析。
```

##### **关于 cbv**

  第一步请求过来之后，执行**dispatch方法** 方法。来区分到底是 **get,post,put,delete** 是通过**反射**找的。


## 二：基于 Django 做 api
  - FBC
  - CBV
```python
# 在 restframework 里面，最重要的四步(全在第二大步，initial函数中处理)：
        # 2.1 处理版本信息
        version, scheme = self.determine_version(request, *args, **kwargs)
        request.version, request.versioning_scheme = version, scheme

        # Ensure that the incoming request is permitted
        # 2.2 认证
        self.perform_authentication(request)
        # 2.3 权限
        self.check_permissions(request)
        # 2.4 限流，对请求用户访问频率的限制。
        self.check_throttles(request)
```

#### 补充：
```
csrf_exempt：屏蔽 csrf 验证
```

自定制验证规则の流程：
```python
第1步：
def perform_authentication(self, request):
    request.user
第2步：调用 user
点进去看，最开始没有 user 值。
将 user 和 auth 设置到 _request里面去了。这个_request 是最原始的。

```
```python
用户请求刚进来，执行 hostview 的 dispatch 方法，
在 dispatch 方法里面，又调用了其他方法。
这里面的 request=Request()

然后执行initial，算了认证流程我写在下面，好好写。
```

## 4. 基于 token 的认证。
```python
算了，我想画图，看我博客好吧。
给你链接：本章末尾
```


补充一个全局的认证和局部的认证。
看代码:
##### 全局：
```python
# views 下
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

class HostView(APIView):
    def get(self,request,*args,**kwargs):
        # 原来的 request 对象：django.core.handlers.wsgi.WSGIRequest
        # 现在的 request 对象：rest_framework.request.Request
        # self.dispatch(request)
        # print(request.user)
        # print(request.token)
        return Response('刘 gay 日华是狗🐶🐶🐶🐶🐶🐶')
```
###### 然后新创建一个 utils.py 文件
```python
from rest_framework.authentication import SessionAuthentication
from rest_framework.authentication import BasicAuthentication
from rest_framework.authentication import BaseAuthentication
from rest_framework.request import Request
from rest_framework.exceptions import APIException
from app01 import models



class MyAuthentication(BaseAuthentication): # 注意看：继承的 BaseAuthentication
    def authenticate(self, request):
        print('2222222222')
        token = request.query_params.get('token')
        obj = models.UserInfo.objects.filter(token=token).first()
        print(token, obj.token)
        if obj:
            return (obj.username,obj)
            # Authenticate the request and return a two-tuple of (user, token).
        raise APIException('用户认证失败')

```
##### 最后一步：在 settings 里面注册下好不好
```python
REST_FRAMEWORK = {
                    'UNAUTHENTICATED_USER': None,
                    'UNAUTHENTICATED_TOKEN': None,
                    "DEFAULT_AUTHENTICATION_CLASSES": [
                        "app01.utils.MyAuthentication",
                    ],
					}
```
完事。 上面三段是关于全局的，意在用户每申请访问一个 url，都要经过我 utils 判断是否携带 token。
  - 如果写到这步，运行报错，看下你的 settings 里面,在INSTALLED_APPS下把这句加上。
```python
'rest_framework',
```
> 全局验证分析:
> AuthView 类里面，authentication_classes = []。这句的意义在于。首次登陆时，用户啥都没干呢，服务器怎么可能拿到 token，你就直接给人返回一个'用户认证失败！'，这样真的好吗兄弟。为空就相当于是免死金牌，可以进入当前要访问的 url。
> 看清楚在 utils 里面继承的是哪个类啊，别搞错了，要严谨。

###### 看没看懂就这样吧，反正我觉得我稍微理解了 哈哈哈哈哈哈哈。

##### 来，进入局部认证。如果上面有点迷，两个结合起来看，让程序跑一跑理解起来会好点。


局部认证代码：
```python
class MyAuthentication(object):
    def authenticate(self,request):
        token = request.query_params.get('token')
        if token == 'ff':
            return ('666','777')
        raise APIException('sorry!')


class Hostview(APIView):
    authentication_classes = [MyAuthentication]   # 在 dispatch 里面调用
    def get(self,request,*args,**kwargs):
        print(request)
        print(request.user)
        print(request.auth)
        return HttpResponse('..')
```
> 这段代码，全部在 views 文件里面，
> 只在 hostview 认证。
> OK  我累了，把 dispatch 图画了。
> MindNode 不知道怎么贴链接。回头我整理到博客，地址放出来。

# day2 关于认证、权限、限流
# day2_note

### 内容回顾： 

第一天的调用模式，就是之后学习他的调用模式。

权限
限流，访问频率
版本

中间件和 rfw 关系？
  - 半毛钱关系都没有
  - 所有的rfw框架都是从 dispatch 开始的。

在 dispatch 里面，执行了 inistal 里面的四个方法：
  1. 处理版本信息
  2. 认证
  3. 权限
  4. 限制访问频率。

关于认证：
  - 编写类：
    - def auth...():
      - None。
      - (user,auth)
      - raise APIException
  - 应用
    - 单独视图
    - 全图

## 今日内容

权限一般情况下会和认证 在一起工作。

1. 认证：检查用户是否存在，如果存在 request.user/request.auth
2. 权限
  - request.user/request.auth 返回一个 True/False。然后看它是否可以继续往下走。

3. 访问频率
### 为什么要限制访问频率？
 - 第一点：爬虫，反爬
 - 第二点：控制 API 访问次数
   - 登录用户的用户名可以做标识
   - 匿名用户可以参考 ip，但是 ip可以加代理。
   - so...只要你想爬，早晚有一天可以爬。

#### 限流的原理
```python
div= {
  '1.1.1.1' : [date3,date2,date1]
  '1.1.1.2' : [date33,date22,date11]
    }
```
```python
# 关于爬虫
  匿名用户：你限制不了，人家可以使用代理
  登录用户：可以通过用户名，注册手机号等手段，但是人家还是可以买多个号。
```

4. 总结
  - 关于认证
```python
- 类：authenticate/authenticate_header
- 返回值：None,(user,auth),raise 异常
- 配置:
  - 视图：
    class IndexView(APIView):
		      authentication_classes = [MyAuthentication,]
	- 全局：
    REST_FRAMEWORK = {
        'UNAUTHENTICATED_USER': None,
        'UNAUTHENTICATED_TOKEN': None,
        "DEFAULT_AUTHENTICATION_CLASSES": [
          # "app02.utils.MyAuthentication",
        ],
    }
```
  - 关于权限
```python
- 类：has_permission/has_object_permission
- 返回值： True、False、exceptions.PermissionDenied(detail="错误信息")
- 配置：
  - 视图：
    class IndexView(APIView):
      permission_classes = [MyPermission,]
  - 全局：
    REST_FRAMEWORK = {
        "DEFAULT_PERMISSION_CLASSES": [
          # "app02.utils.MyAuthentication",
        ],
    }
```
  - 关于限流
```python
- 类：allow_request/wait PS: scope = "user_ff"
- 返回值：True、False
- 配置： 
  - 视图： 
    class IndexView(APIView):
      throttle_classes=[AnonThrottle,UserThrottle,]
      def get(self,request,*args,**kwargs):
        self.dispatch
        return Response('访问首页')
  - 全局
    REST_FRAMEWORK = {
      "DEFAULT_THROTTLE_CLASSES":[

      ],
      'DEFAULT_THROTTLE_RATES':{
        'anon_ff':'5/minute',
        'user_ff':'10/minute',
      }
    }
```
