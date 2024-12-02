#from msilib.schema import ListView

from django.http.response import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.

from django.views import View


#验证模块添加
from django.contrib.auth.mixins import LoginRequiredMixin
#MEDIA模块添加
from django.conf import settings
#分页模块
from django.core.paginator import Paginator
#下载模块
from django.http import FileResponse, Http404
import os
from django.shortcuts import get_object_or_404
import mimetypes


from .models import FileModel

'''
产品线界面
'''
#12.文件下载功能？应该是前端的事？

class InfoView(LoginRequiredMixin,View):
    
    #未验证成功，返回这个界面
    def handle_no_permission(self):
        return render(self.request, 'no_permission.html')
    
    def get(self, request):
        #添加分类模块
        category = request.GET.get('category','all')
        #根据分类筛选
        if category and category != 'all':
            files = FileModel.objects.filter(file_dist=category).order_by('-id')
        else:
            files = FileModel.objects.all().order_by('-id')
        
         #每页显示数量
        page_size = 6
        paginator = Paginator(files, page_size)
        page = request.GET.get('page', 1)

        try:
            #获取当前页的数据
            current_page = paginator.page(page)
            files_page = current_page.object_list
        except:
            current_page = paginator.page(1)
            files_page = current_page.object_list

        context = {
            'page_size': page_size,
            'files': files_page,
            'total_files': len(files),
            'username': request.user.username,
            'MEDIA_URL': settings.MEDIA_URL,
            'current_category': category,
        }

        return render(request, "product.html", context)


    #文件下载，添加下载视图


class FileDownloadView(View):

    MIME_TYPES = {
        '.pdf': 'application/pdf',
        '.doc': 'application/msword',
        '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        '.xls': 'application/vnd.ms-excel',
        '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        '.ppt': 'application/vnd.ms-powerpoint',
        '.pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation'
    }

    def get(self, request, file_id):
        file_obj = get_object_or_404(FileModel, id=file_id)
        file_path = file_obj.file.path

        try:
            filename = os.path.basename(file_path)
            ext = os.path.splitext(filename)[1].lower()

            # 获取 MIME 类型
            content_type = self.MIME_TYPES.get(ext) or mimetypes.guess_type(file_path)[0]

            response = FileResponse(open(file_path, 'rb'))
            response['Content-Type'] = content_type
            response['Content-Disposition'] = f'attachment; filename="{filename}"'

            return response

        except FileNotFoundError:
            raise Http404("文件未找到")


