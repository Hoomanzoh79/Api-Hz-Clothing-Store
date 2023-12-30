from django.contrib import admin
from .models import Cloth,Comment

@admin.register(Cloth)
class ClothAdmin(admin.ModelAdmin):
    list_display = ['title','author','price', 'active', 'season', 'gender', ]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["cloth","author","body","active",]