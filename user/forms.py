# -*- coding: utf-8 -*-

from django import forms
from django.core.validators import RegexValidator
from .models import *



#验证注册
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
    



#验证登录
class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=5)

#用于修改登录用户的昵称和科室所属
class UserForm(forms.ModelForm):  
    class Meta:  
        model = UserProfile  
        fields = ['username', 'department']  
        
    def clean_username(self):  
        username = self.cleaned_data.get('username')  
        if len(username) < 2:  
            raise forms.ValidationError("用户名长度太短")  
        return username


#验证头像上传
class UploadImageForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['avatar']


#暂时消除
#验证密码正确
# class ModifyPwdForm(forms.Form):
#     password1 = forms.CharField(required=True, min_length=5)
#     password2 = forms.CharField(required=True, min_length=5)
