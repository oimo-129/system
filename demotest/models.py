# _*_ encoding:utf-8 _*_
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

# Create your models here.

from django.db import models

#设置进入哈希验证
from django.contrib.auth.hashers import make_password, check_password

#测试登录的用户信息

class UserTest(AbstractUser):


#class UserTest(models.Model):

    GENDER_CHOICES = [
        ('male', '男'),
        ('female', '女')
    ]

    #username = models.CharField(max_length=10, unique=True)

    #password = models.CharField(max_length=100)


    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)
    # 允许性别字段为空

    # 添加 related_name 参数以避免冲突
    groups = models.ManyToManyField(
        Group,
        related_name='user_test_set',  # 自定义反向访问器名称
        blank=True
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='user_test_set_permissions',  # 自定义反向访问器名称
        blank=True
    )

    def __str__(self):
        return self.username

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)




## 图片
class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')
