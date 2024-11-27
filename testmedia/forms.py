#表单中处理文件的上传
from django import forms
from .models import MyModel


class MyForm(forms.ModelForm):
    class Meta:
        model = MyModel
        fields = ['title', 'file']