from django.contrib import admin
from .models import Cart,CartItem

class CartItemInline(admin.TabularInline):
    model = CartItem
    fields = ['id', 'cloth', 'quantity']
    extra = 0
    min_num = 1


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_at']
    inlines = [CartItemInline]