from django.contrib import admin
from . models import * 

# Register your models here.


class LayoutImageInline(admin.TabularInline):
    model = LayoutImage

@admin.register(Socials)
class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Layout)
class LayoutAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at', 'is_active']
    list_filter = ['name', 'created_at', 'is_active']
    list_editable = ['is_active']
    prepopulated_fields = {
                            "slug" : ("title",),}
    inlines = [LayoutImageInline, ]

