from django.http import HttpResponseForbidden
import hashlib
import uuid

def get_unique_str():
#     拿到uuid4的字符串
    uuid_str = str(uuid.uuid4()).encode("utf-8")
# 使用md5摘要
    md5 = hashlib.md5()
    md5.update(uuid_str)
# 返回十六进制的字符
    return md5.hexdigest()


def checkout_permission(permission):

    def outter(func):
        def inner(request, *args, **kwargs):
        #     判断权限
            user = request.user
            # 先判断是不是登录
            if user.is_anonymous:
                return HttpResponseForbidden("未登录 无权限")
            # 再判断权限够不够
            if user.permission & permission == permission:
                return func(request, *args, **kwargs)
            else:
                return HttpResponseForbidden("您无权限 请联系管理员")
        return inner
    return outter