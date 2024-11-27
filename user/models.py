# _*_ encoding:utf-8 _*_

from django.db import models

from django.contrib.auth.models import AbstractUser
# Create your models here.


'''
科室表
'''
class Department(models.Model):
    name = models.CharField(max_length=100, unique=True, blank=True, null=True, default='未设置', verbose_name="科室")

    class Meta:
        verbose_name = "部门表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


'''
用户信息表
'''
class UserProfile(AbstractUser):
    department = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True, blank=True, default=1, verbose_name="科室名称")
    #department = models.CharField(max_length=100)
    #上传头像模块
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True, verbose_name="头像")

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username  #返回用户名作为对象的字符串表示

