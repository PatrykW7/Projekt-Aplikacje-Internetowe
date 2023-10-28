from django.contrib import admin

# Register your models here.

# Zaimportowanie tabeli Category
from .models import Category, AiModel

admin.site.register(Category)
admin.site.register(AiModel)