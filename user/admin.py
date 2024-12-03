from django.contrib import admin  
from django.contrib.auth.admin import UserAdmin  
from django.utils.translation import gettext_lazy as _  
from django.contrib.auth.hashers import make_password  
from django.utils.html import format_html  
from .models import UserProfile, Department  

class CustomUserAdmin(UserAdmin):  
    # 列表页显示的字段  
    list_display = ('username', 'email', 'get_department', 'show_avatar', 'is_active', 'is_staff')  
    # 列表页可以直接编辑的字段  
    list_editable = ('is_active',)  
    # 列表页的过滤器  
    list_filter = ('is_active', 'is_staff', 'department', 'date_joined')  
    # 搜索字段  
    search_fields = ('username', 'email', 'department__name')  
    # 排序方式  
    ordering = ('-date_joined',)  
    
    # 编辑页面的字段分组  
    fieldsets = (  
        (None, {'fields': ('username', 'password')}),  
        (_('个人信息'), {'fields': ('email', 'department', 'avatar')}),  
        (_('权限信息'), {  
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),  
        }),  
        (_('重要日期'), {'fields': ('last_login', 'date_joined')}),  
    )  
    
    # 添加用户页面的字段分组  
    add_fieldsets = (  
        (None, {  
            'classes': ('wide',),  
            'fields': ('username', 'email', 'department', 'password1', 'password2'),  
        }),  
    )  
    
    # 自定义操作  
    actions = ['reset_password']  
    
    def get_department(self, obj):  
        """获取部门名称"""  
        return obj.department.name if obj.department else '未设置'  
    get_department.short_description = '所属科室'  
    get_department.admin_order_field = 'department__name'  
    
    def show_avatar(self, obj):  
        """显示头像"""  
        if obj.avatar:  
            return format_html('<img src="{}" width="32" height="32" style="border-radius: 50%;" />',   
                             obj.avatar.url)  
        return '无头像'  
    show_avatar.short_description = '头像'  
    
    def reset_password(self, request, queryset):  
        """重置密码操作"""  
        updated = 0  
        for user in queryset:  
            user.password = make_password('123456')  
            user.save()  
            updated += 1  
        self.message_user(request, f'成功重置 {updated} 个用户的密码为: 123456')  
    reset_password.short_description = '重置所选用户密码为123456'  
    
    def save_model(self, request, obj, form, change):  
        """保存模型时的额外操作"""  
        # 如果是新建用户，确保密码被正确加密  
        if not change:  
            obj.set_password(form.cleaned_data["password1"])  
        super().save_model(request, obj, form, change)  

class DepartmentAdmin(admin.ModelAdmin):  
    list_display = ('name', 'is_default', 'user_count')  
    list_filter = ('is_default',)  
    search_fields = ('name',)  
    
    def user_count(self, obj):  
        """显示部门下的用户数量"""  
        return obj.userprofile_set.count()  
    user_count.short_description = '用户数量'  
    
    def save_model(self, request, obj, form, change):  
        """保存部门时的额外操作"""  
        # 如果设置为默认部门，取消其他部门的默认状态  
        if obj.is_default:  
            Department.objects.exclude(pk=obj.pk).update(is_default=False)  
        super().save_model(request, obj, form, change)  

# 注册模型到admin  
admin.site.register(UserProfile, CustomUserAdmin)  
admin.site.register(Department, DepartmentAdmin)