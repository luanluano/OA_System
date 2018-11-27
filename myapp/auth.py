from django.contrib.auth.backends import ModelBackend
from .models import MyUser
class MyBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        # 第一个找人
        try:
            user = MyUser.objects.get(username=username)
        except MyUser.DoesNotExist:
            try:
                user = MyUser.objects.get(phone=username)
            except MyUser.DoesNotExist:
                return None

        # 用于判断is_active字段
        if user.check_password(password) and self.user_can_authenticate(user=user):
            return user