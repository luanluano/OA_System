from django.contrib.auth import authenticate, login, logout
from django.core.cache import caches
from django.core.mail import send_mail
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

# Create your views here.

from django.contrib.auth.models import User
from django.shortcuts import render
from django.template.loader import get_template

from django.views import View

from OA_System import settings
from myapp.models import MyUser
from myapp.util import get_unique_str

# 得到具体的缓存
mycache = caches['mail_cache']


class RegisterAPI(View):

    def post(self, req):
        # 解析参数
        params = req.POST
        name = params.get("name")
        pwd = params.get("pwd")
        confirm_pwd = params.get("confirm_pwd")
        #判断用户密码和确认密码是否一致
        if pwd and confirm_pwd and pwd == confirm_pwd:
            # 判断用户名是否可用
            if MyUser.objects.filter(username=name).exists():
                data = {
                    "code": 2,
                    "msg": "用户名不可用",
                    "data": ""
                }
                return JsonResponse(data)
            else:
                # 创建用户
                user = MyUser.objects.create_user(username=name, password=pwd, is_active=False)
                data = {
                    "code": 1,
                    "msg": "OK",
                    "data": user.id
                }
                return JsonResponse(data)

class LoginAPI(View):

    def get(self, req):
#         解析参数
        param = req.GET
        name = param.get("name")
        pwd = param.get("pwd")
#         校验
        user = authenticate(username=name, password=pwd)
        if user:
            # 登录
            login(req, user)
            return HttpResponse("ok")
        else:
            return HttpResponse("用户名或密码错误")






# 退出登录
def mylogout(req):
    logout(req)
    return HttpResponse("已经退出")


def send_verify_mail(req):
    title = "来自千锋的问候"
    msg = ""
    from_email = settings.DEFAULT_FROM_EMAIL
    recieve = [
        "liuda@1000phone.com"
    ]
    code = get_unique_str()
    # 拼接URL
    url = "http://" + req.get_host() + "/myapp/verify/"+ code
    print(url)
    # 渲染HTML页面
    template = get_template("verify.html")
    html = template.render({"url": url})
    # print(html)
    # 发送邮件
    send_mail(title, msg, from_email, recieve, html_message=html)

    # 将发送的结果保存到缓存
    # 获取请求的用户
    user = req.user
    user_id = user.id #此处应该是真实的用户id
    mycache.set(code, user_id, 60 * 60)
    return HttpResponse("ok")

def verify(req, code):
    # 获取网址后边的路径 字符串

    # 去缓存尝试拿数据
    val = mycache.get(code)
    # 如果能拿到 我们就修改is_active字段
    if val:
        MyUser.objects.filter(pk=int(val)).update(is_active=True)
        mycache.delete(code)
        return HttpResponse("验证成功")
    # 如果没拿到 就告诉他链接无效
    else:
        return HttpResponse("链接无效")