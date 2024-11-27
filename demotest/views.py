from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from demotest.form import UserForm


#登录模块验证依赖
from django.contrib.auth import authenticate, login
from django.http import HttpResponse

from .form import UploadFileForm

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, 'upload_success.html')
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})


def home(request):
    register_form = UserForm(request.POST)
    if register_form.is_valid():
        pass
    register_form = UserForm()
    return render(request, 'test_index.html', {'register_form': register_form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print(username, password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponse('登录成功')
        else:
            return HttpResponse('登录失败')

    return render(request, 'test_login.html')


def resign(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        #制作密码选项




#图片认证模块
