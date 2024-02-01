from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import Cart

@admin.register(Cart)
class CartAdmin(ModelAdmin):
    list_display = ["created_at"]
