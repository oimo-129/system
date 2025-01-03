from django.core.exceptions import ValidationError
from django.db import models

# Create your models here.
import os

from django.utils import timezone

from datetime import datetime
# 项目的第二个应用，用于资源添加处理
#富文本编辑器
from django_ckeditor_5.fields import CKEditor5Field
#from ckeditor.fields import RichTextField
#用于上传文件
def upload_to(instance, filename):
    today = datetime.today()
    return os.path.join(f'files/{today.year}/{today.month}/{today.day}', filename)

'''
首页轮播图
'''
class BannerModel(models.Model):
    #标题
    title = models.CharField(max_length=50, verbose_name="轮播图图片标题")
    #轮播图目标文件
    file_banner = models.FileField(upload_to=upload_to, verbose_name='轮播图目标文件', null=True)
    #图片
    image = models.ImageField(upload_to="banner/%Y/%m", verbose_name="首页轮播图图片")   
    #添加时间决定轮播图样式
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "首页轮播图资源表"
        verbose_name_plural = verbose_name

    #控制model实例的名字
    def __str__(self):
        return self.title




'''
首页左下文件
'''
class File1Model(models.Model):
    #文件
    file1 = models.FileField(upload_to=upload_to, verbose_name = '首页左下文件',null = True)
    
    
    #添加时间
    add_time = models.DateField(default=datetime.now,verbose_name="添加时间")
    
    
    class Meta:
        verbose_name = "首页左下文件表"
        verbose_name_plural = verbose_name

    #控制model实例的名字
    def __str__(self):
       return os.path.basename(self.file1.name)



'''
产品类别表
'''

class ProductCategory(models.Model):
    name = models.CharField(max_length=50, verbose_name='产品类别')

    class Meta:
        verbose_name = '产品类别'
        verbose_name_plural = '产品类别'

    def __str__(self):
        return self.name



'''
产品线页面的资源文件
'''
class FileModel(models.Model):
    name = models.CharField(max_length=50, verbose_name='文件名')
    file = models.FileField(upload_to=upload_to, verbose_name='上传文件', null=True)
    file_dist = models.CharField(verbose_name='文件分类'
                                 , max_length=20,
                                 choices=(('产业洞察', '产业洞察'),
                                          ('行业研究', '行业研究'),
                                          ('用户调研', '用户调研'),
                                          ('院内报告', '院内报告'))
                                 )
    file_product = models.ForeignKey(ProductCategory, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='文件所属产品类型')
    add_time = models.DateTimeField(default=timezone.now, verbose_name='报告时间')
    cover = models.ImageField(upload_to='covers/%Y/%m/%d', verbose_name='文件封面', default='default/default.png')


    # 元数据，控制模型的行为和表现
    class Meta:
        managed = True
        verbose_name = '上传文件'
        verbose_name_plural = '上传文件'

    def __str__(self):
        return self.name




'''
    点击链接，显示管理员编辑好的新闻内容    
'''
class News(models.Model):
    title = models.CharField('标题', max_length=200)
    content = CKEditor5Field('内容', config_name='default')
    #content = RichTextField('新闻内容')
    image = models.ImageField('新闻图片', upload_to='news_images/')
    pub_date = models.DateTimeField('发布时间', auto_now_add=True)
    
     
    class Meta:
        ordering = ['-pub_date']
        verbose_name = '新闻'
        verbose_name_plural = '新闻管理'

    def __str__(self):
        return self.title
    
