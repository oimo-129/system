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
import json


#添加前端静态路由的配置
from itproject.settings import MEDIA_ROOT, MEDIA_URL
from django.conf import settings

#首页的资源载入，选择文件类
from info.models import *

#分页功能
from django.core.paginator import Paginator

#消息提示
from django.contrib import messages


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
        
        #左下文件，分页模块
        page = request.GET.get('page',1)
        
        #轮播图资源
        all_banners = BannerModel.objects.all().order_by('-add_time')
        #添加新闻列表
        news_items = News.objects.all().order_by('-pub_date')
        #左侧文件资源
        all_file1s = File1Model.objects.all().order_by('-add_time')
        #近期文档文件
        all_files = FileModel.objects.all().order_by('-add_time')
        
        file1_names = [os.path.splitext(os.path.basename(file.file1.name))[0] for file in all_file1s]
        #分页器，显示5个
        paginator = Paginator(list(zip(all_file1s,file1_names)),5)
        
        try:
            current_page = paginator.page(page)
        except PageNotAnInteger:
        # 如果页码不是整数，返回第一页
            current_page = paginator.page(1)
        except EmptyPage:
        # 如果页码超出范围，返回第一页
            current_page = paginator.page(1)
       
       
        numbers = range(1,9)
        context = {
            'all_banners': all_banners,
            #'all_file1s':all_file1s,
            'MEDIA_URL': settings.MEDIA_URL,
            'numbers': numbers,
           # 'file1_names': file1_names,
            'current_page':current_page,
            'total_pages':paginator.num_pages,
            'news_items':news_items,
            #最近的报告文件
            'all_files':all_files,
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
        desp_back = Department.objects.all()
        context = {
            'register_form': register_form,
            'desp_back': desp_back,
        }
        return render(request, "resign.html", context)

    def post(self, request):
        register_form = ResignForm(request.POST)
        if register_form.is_valid():
            email_num = request.POST.get("email", " ")
            
            if UserProfile.objects.filter(email=email_num).exists():
                return render(request, "resign.html", {'register_form': register_form, 'msg': "邮箱号已被使用"})
         
            user_name = request.POST.get("username", "")
            desp_id = request.POST.get("department", "")
            desp_name = Department.objects.get(id=desp_id)
            pass_word = request.POST.get("password", "")
            #创建用户
            user_profile = UserProfile(
                email= email_num,
                username= user_name,  
                desp_name= desp_name,
            )
            #密码，这里还是用密文比较好
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


'''
个人中心模块
'''

 
class UserUpdateForm(forms.ModelForm):  
    class Meta:  
        model = UserProfile  
        fields = ['username', 'desp_name']  

    def clean_username(self):  
        username = self.cleaned_data.get('username')  
        if not username:  
            raise forms.ValidationError("用户名不能为空")  
        if UserProfile.objects.exclude(id=self.instance.id).filter(username=username).exists():  
            raise forms.ValidationError("该用户名已被使用")  
        return username 


class UserInfoView(LoginRequiredMixin,View):
    def get(self, request):

        desp_back = Department.objects.all()
        context = {
                'username': request.user.username,
                'desp_front': desp_back,
                'email_front': request.user.email,
                'MEDIA_URL': settings.MEDIA_URL,
            }

        return render(request, "usercenter.html", context)
    
    def post(self, request):  
        # 创建一个新的字典来存储处理后的数据  
        processed_data = request.POST.copy()  
        
        # 如果有desp_id，将其转换为desp_name  
        desp_id = request.POST.get('desp_id')  
        if desp_id:  
            try:  
                department = Department.objects.get(id=desp_id)  
                processed_data['desp_name'] = department.id  # 使用部门ID  
            except Department.DoesNotExist:  
                return JsonResponse({  
                    'status': 'error',  
                    'message': '所选科室不存在'  
                })  

        form = UserUpdateForm(processed_data, instance=request.user)  
        if form.is_valid():  
            form.save()  
            return JsonResponse({  
                'status': 'success',  
                'message': '修改成功！'  
            })  
        else:  
            error_msg = next(iter(form.errors.values()))[0]  
            return JsonResponse({  
                'status': 'error',  
                'message': error_msg  
            })  






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


#修改用户密码Ajax方式提交

class UpdatePwdView(LoginRequiredMixin, View):  
    """个人中心修改用户密码"""  
    # def post(self, request):  
    #     pwd1 = request.POST.get("password1", "")  
    #     pwd2 = request.POST.get("password2", "")  
        
    #     # 表单验证  
    #     if not pwd1 or not pwd2:  
    #         return JsonResponse({'status': 'fail', 'msg': '密码不能为空'})  
            
    #     if len(pwd1) < 6 or len(pwd1) > 20:  
    #         return JsonResponse({'status': 'fail', 'msg': '密码长度应在6-20位之间'})  
            
    #     if pwd1 != pwd2:  
    #         return JsonResponse({'status': 'fail', 'msg': '两次输入的密码不一致'})  

    #     try:  
    #         user = request.user  
    #         user.set_password(pwd2)  # 使用set_password而不是make_password  
    #         user.save()  
    #         return JsonResponse({'status': 'success'})  
    #     except Exception as e:  
    #         return JsonResponse({'status': 'fail', 'msg': '服务器错误，请稍后重试'})  


'''
情报需求，前端提交验证的表单，后台接收数据，在info文件夹下生成excel表单

'''
class UserInfoNeed(LoginRequiredMixin, View):
    
    def handle_no_permission(self):
        return render(self.request, 'no_permission.html')
    
    def get(self, request):

        desp_back = Department.objects.values('name')

        context = {
            'username': request.user.username,
            'desp_front': desp_back,
            'email_front': request.user.email,
            'MEDIA_URL': settings.MEDIA_URL,
        }

        return render(request, 'center_need.html', context)

    def post(self, request):
            try:
            # 创建新的需求表单记录
                need_form = NeedForm(
                    user=request.user,
                    section=request.POST.get('section'),
                    analysis_type=request.POST.get('analysis_type'),
                    analysis_detail=request.POST.get('analysis_detail'),
                    urgency=request.POST.get('urgency'),
                    content=request.POST.get('content'),
                    department=request.POST.get('department'),
                    contact_person=request.POST.get('contact_person'),
                    contact_info=request.POST.get('contact_info')
                )
                need_form.save()
            
            # 添加成功消息
                messages.success(request, '需求表单提交成功！')
                return redirect('user:need')  # 重定向到需求页面
                
            except Exception as e:
                # 如果保存失败，添加错误消息
                messages.error(request, f'提交失败：{str(e)}')
                
                # 返回表单页面，保留用户输入的数据
                desp_back = Department.objects.values('name')
                context = {
                    'username': request.user.username,
                    'desp_front': desp_back,
                    'email_front': request.user.email,
                    'MEDIA_URL': settings.MEDIA_URL,
                    'form_data': request.POST,  # 保留用户输入的数据
                    'error': str(e)
                }
                return render(request, 'center_need.html', context)


