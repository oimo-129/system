# -*- coding: utf-8 -*-

from django import forms
from captcha.fields import CaptchaField

from .models import *

#注册表单的校验

class ResignForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=6, max_length=20)
    captcha = CaptchaField()


#登录表单的校验
#用modelForm进行尝试
# class LoginForm(forms.ModelForm):
#
#     class Meta:
#         model = UserProfile
#         fields = ['username', 'password']
#


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=5)


class UserForm(forms.ModelForm):
    username = forms.CharField(max_length=30, required=True)
    desp_name = forms.ModelChoiceField(queryset=Department.objects.all(), label='科室')



#将头像上传到这个文件夹
# class ImageUploadForm(forms.ModelForm):
#     class Meta:
#         model = UserForm
#         fields = ['avatar']