# myapp/views.py  

from django.http import JsonResponse
from django.shortcuts import render
from django.views import View  
from .forms import ContactForm  

class ContactView(View):
    def get(self, request):
        return render(request,  'test_ajax.html', {})

    def post(self, request):  
        form = ContactForm(request.POST)  
        if form.is_valid():  
            form.save()  
            return JsonResponse({'status': 'success', 'message': 'ajax提交到数据到后台!'})
        return JsonResponse({'status': 'error', 'message': 'Invalid data'})