from django.contrib import admin
from . models import * 

# Register your models here.


class ProductImageInline(admin.TabularInline):
    model = ProductImage

@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    prepopulated_fields = {
                            "slug" : ("name",),}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at', 'is_active', 'is_feature', 'is_trending']
    list_filter = ['is_active', 'is_feature', 'is_trending']
    list_editable = ['is_active','is_feature', 'is_trending']
    prepopulated_fields = {
                            "slug" : ("name",),}
    inlines = [ProductImageInline, ]

