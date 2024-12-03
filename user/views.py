from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect

from django.views import View

from .models import *

from .forms import *

#登录模块添加
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.urls import reverse

from django.contrib.auth.hashers import make_password, check_password

#验证模块添加
from django.contrib.auth.mixins import LoginRequiredMixin

#json处理前端，异步，ajax启动
from django.http import JsonResponse

#添加前端静态路由的配置
from itproject.settings import MEDIA_ROOT, MEDIA_URL
from django.conf import settings

#首页的资源载入
from info.models import *


#登录验证函数

#登录验证
class CustomBackend(ModelBackend):

    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None



'''
系统首页设置
'''
class IndexView(View):
    def get(self, request):

        #轮播图资源
        all_banners = BannerModel.objects.all().order_by('index')
        numbers = range(1,9)
        context = {
            'all_banners': all_banners,
            'MEDIA_URL': settings.MEDIA_URL,
            'numbers': numbers,
        }

        return render(request, "index.html", context)






'''
登录视图
'''
class LoginView(View):
    def get(self, request):
        return render(request, "login.html", {})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            #登录验证
            user_name = request.POST.get('username', "")
            password = request.POST.get('password', "")


           #这一步验证错误，总是null
            user = authenticate(username=user_name, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse("home"), {'MEDIA_URL': settings.MEDIA_URL})
            else:
                msg_error = "登录验证失败"
                return render(request, "login.html", {"msg": msg_error})            
        else:
            return render(request, "login.html", {"login_form": login_form})


'''
注册视图
'''
class RegisterView(View):

    def get(self, request):
        register_form = ResignForm()
        return render(request, "resign.html", {'register_form': register_form})

    def post(self, request):
        register_form = ResignForm(request.POST)
        if register_form.is_valid():
            email_num = request.POST.get("email", " ")
            
            if UserProfile.objects.filter(email=email_num).exists():
                return render(request, "resign.html", {'register_form': register_form, 'msg': "邮箱号已被使用"})
            
            #添加默认科室设置
            default_department = Department.objects.filter(is_default=True).first()
            
            if not default_department:
                default_department = Department.objects.create(
                    name="默认科室",
                    is_default = True
                )
                
            pass_word = request.POST.get("password", "")
            #创建用户
            user_profile = UserProfile(
                email= email_num,
                username= email_num,
                department = default_department
            )
            #密码，应该是这里要修改
            user_profile.password = make_password(pass_word)
            user_profile.save()
            return render(request, "resign.html", {'register_form': register_form, 'msg': "用户注册成功!!!"})
        else:
            return render(request, "resign.html", {"register_form": register_form})


'''
退出模块
'''

class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse("home"))



# 图片模块载入

'''
1.setting,
MEDIA
MEDIA_ROOT
2.url 
3.重写前端界面

'''
# class UploadImgView(View):
#     #只需要定义post方法
#     def post(self,request):
#         image_form = ImageUploadForm(request.POST, request.FILES, instance=request.user)
#         if image_form.is_valid():
#             return HttpResponse("图片信息合法")
#         else:
#             return HttpResponse("哪里有错误")
#
#






'''
个人中心模块
'''
class UserInfoView(LoginRequiredMixin,View):
    def get(self, request):

        desp_back = Department.objects.values('name')


        context = {
                'username': request.user.username,
                'desp_front': desp_back,
                'email_front': request.user.email,
                'MEDIA_URL': settings.MEDIA_URL,
            }

        #return render(request, 'my_template.html', context)

        return render(request, "usercenter.html", context)

    #对个人数据进行保存

    #对科室进行修改
    def post(self, request):
        #修改相应对象
        mody_form = UserForm(request.POST)
        if mody_form.is_valid():
            username = mody_form.cleaned_data['username']
            department = mody_form.cleaned_data['desp_name']
            print("用户名:", username)
            print("科室的内容：", department.name)
            return HttpResponse("用户信息修改成功")
        else:
            return render(request, "usercenter.html", {"mody_form": mody_form})



#修改用户头像Ajax方式提交
class UploadImageView(LoginRequiredMixin,View):

    def post(self,request):       
        #对图片进行验证
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            image_form.save()
            return JsonResponse({
                'status': 'success',
                'msg': '头像上传成功！',
                'avatar_url': request.user.avatar.url
            })
        return JsonResponse({
            'status':'fail',
            'msg':'头像上传失败！'
        })





#回退显示所有表
class ShowDep(View):

    def get(self, request):
           # desp_back = Department.objects.values('name')

            #print(desp_back)
            #return render(request, "listdep.html", {'desp_front': desp_back})
            return render(request,"boot_login.html",{})

'''
1.前端界面，一个label ,for循环

   
2.后端调数据库，拿到数据库
3.后端带数据返回前端
'''


'''
情报需求，前端提交验证的表单，后台接收数据，在info文件夹下生成excel表单

'''
class UserInfoNeed(LoginRequiredMixin, View):
    def get(self, request):

        desp_back = Department.objects.values('name')

        context = {
            'username': request.user.username,
            'desp_front': desp_back,
            'email_front': request.user.email,
            'MEDIA_URL': settings.MEDIA_URL,
        }

        return render(request, 'center_need.html', context)

        #return render(request, "center_need.html", {})

