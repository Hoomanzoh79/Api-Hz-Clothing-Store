from django.contrib import admin
from .models import Cloth

@admin.register(Cloth)
class ClothAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'active', 'season', 'gender', ]