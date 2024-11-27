# from django.db import models
#
# # Create your models here.
#
# class MyModel(models.Model):
#     title = models.CharField(max_length=100)
#     file = models.FileField(upload_to='uploads/')
#
#     def __str__(self):
#         return self.title
#



from django.db import models
from django.contrib import admin

# 用于测试MEDIA的表
class TestMedia(models.Model):
    # 该字段将存储上传的图片路径
    image = models.ImageField(upload_to='picture/%Y-%m')

    def __str__(self):
        self.name = "TestMedia_picture"
        return self.name


# 装饰器,作用：将模型TestMedia注册到admin后台，用于显示该表的信息
admin.site.register(TestMedia)