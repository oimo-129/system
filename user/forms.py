# -*- coding: utf-8 -*-

from django import forms
from captcha.fields import CaptchaField
from django.core.validators import RegexValidator
from .models import *




class ResignForm(forms.Form):
    email = forms.EmailField(
                            required=True,
                             validators=[
                                 RegexValidator(
                                     regex=r'^[a-zA-Z0-9_.+-]+@gree\.com$',
                                     message='不符合格力内邮账号样式',
                                     code = 'invalid_email'
                                 )
                             ],
                             error_messages={  
                                'required': '请输入邮箱地址',  
                                'invalid': '请输入有效的邮箱地址'  
                            }  
                            )
    password = forms.CharField(
                        required=True,
                        min_length=6, 
                        max_length=20,
                        error_messages={
                             'required': '请输入密码',  
                             'min_length': '密码长度至少为6位',  
                             'max_length': '密码长度不能超过20位'  
                        })
    
    #captcha = CaptchaField()


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