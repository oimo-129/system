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
        files = FileModel.objects.all().order_by('-id')
         #每页显示数量
        page_size = 2
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













    # def get(self, request, file_id):
    #
    #
    #     # 根据文件 ID 获取文件对象
    #     file_obj = get_object_or_404(FileModel, id=file_id)
    #
    #     # 获取文件路径
    #     file_path = file_obj.file.path
    #
    #     try:
    #         # 获取文件名和扩展名
    #         filename = os.path.basename(file_path)
    #         ext = os.path.splitext(filename)[1].lower()
    #         # 设置正确的 MIME 类型
    #         content_type = None
    #         if ext == '.pdf':
    #             content_type = 'application/pdf'
    #         elif ext in ['.doc', '.docx']:
    #             content_type = 'application/msword'
    #         elif ext in ['.xls', '.xlsx']:
    #             content_type = 'application/vnd.ms-excel'
    #         elif ext in ['.ppt', '.pptx']:
    #             content_type = 'application/vnd.ms-powerpoint'
    #         else:
    #             # 使用 mimetypes 模块猜测 MIME 类型
    #             content_type, _ = mimetypes.guess_type(file_path)
    #
    #             # 打开文件并创建响应
    #         file = open(file_path, 'rb')
    #         response = FileResponse(file)
    #
    #         # 设置响应头
    #         response['Content-Type'] = content_type
    #         response['Content-Disposition'] = f'attachment; filename="{filename}"'
    #
    #
    #         # 返回文件响应
    #        # response = FileResponse(open(file_path, 'rb'), as_attachment=True, filename=file_obj.name)
    #         return response
    #
    #
    #     except FileNotFoundError:
    #         raise Http404("文件未找到？？？")
