from django.contrib import admin

from .models import Order, OrderItem


@admin.register(Order)
class OrderTypeAdmin(admin.ModelAdmin):
    list_display = ['created', 'first_name', 'last_name', 'phone', 'order_key']
    list_filter = ['order_key']

@admin.register(OrderItem)
class OrderItemTypeAdmin(admin.ModelAdmin):
    list_display = ['order', 'id', 'product', 'quantity']
