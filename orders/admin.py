from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    list_display = ['order', 'cloth', 'quantity', 'price', ]
    extra = 0
    min_num = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['customer', 'first_name', 'last_name', 'datetime_created', 'is_paid','is_cancelled']
    inlines = [
        OrderItemInline
    ]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'cloth', 'quantity', 'price', ]