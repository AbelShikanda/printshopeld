from django.contrib import admin

# Register your models here.

from .models import UserBase

@admin.register(UserBase)
class UserBaseAdmin(admin.ModelAdmin):
    list_display = ['user_name', 'email','is_active', 'phone', 'town', 'is_staff']