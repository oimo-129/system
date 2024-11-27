from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from .models import UserTest  # 导入你指定的用户模型

class CustomAuthBackend(BaseBackend):
   #异常捕获机制的理解与使用
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # 尝试从指定的模型中获取用户
            user = UserTest.objects.get(username=username)

            # 检查密码是否正确
            if user.check_password(password):  # 你的自定义模型需要实现 check_password 方法
                return user
        except UserTest.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return UserTest.objects.get(pk=user_id)
        except UserTest.DoesNotExist:
            return None