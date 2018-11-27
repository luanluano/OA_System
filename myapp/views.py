from django.contrib.auth import authenticate, login
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

# Create your views here.

from django.contrib.auth.models import User
from django.shortcuts import render

from django.views import View

class RegisterAPI(View):

    def post(self,req):
        #解析参数
        params = req.POST
        name = params.get("name")
        pwd = params.get("pwd")
        confirm_pwd = params.get("confirm_pwd")
        #判断用户密码和确认密码是否一致
        if pwd and confirm_pwd and pwd==confirm_pwd:
            # 判断用户名是否可用
            if User.objects.filter(username=name).exists():
                data ={
                    'code':2,
                    'msg':"用户名不可用",
                    'data':""
                }
                return JsonResponse(data)
            else:
                # 创建用户
                user = User.objects.create_user(username=name,password=pwd)
                data = {
                    'code':1,
                    'msg':'OK',
                    'data':user.id

                }
                return JsonResponse(data)

class LoginAPI(View):

    def get(self,req):
        #解析参数
        param = req.GET
        name = param.get("name")
        pwd = param.get("pwd")
        #校验
        user = authenticate(username = name,password = pwd)
        if user:
            #登入
            login(req,user)
            return HttpResponse("ok")
        else:
            return HttpResponse("用户名或密码错误")



