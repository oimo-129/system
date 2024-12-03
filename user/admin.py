from django.contrib import admin

# Register your models here.
#注册用户表

from .models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    pass

admin.site.register(UserProfile, UserProfileAdmin)