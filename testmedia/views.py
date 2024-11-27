from django.shortcuts import render

# Create your views here.
'''
media使用
1.setting
2.model
3.form
4.view
5.template

'''
from django.shortcuts import render, redirect
from .forms import MyForm



def upload_file(request):
    if request.mothod == 'POST':
        form = MyForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = MyForm()
    return render(request, 'test_upload.html', {'form': form})

