from django.contrib import admin

# Register your models here.

# Zaimportowanie tabeli Category
from .models import Categorie, AiModel

admin.site.register(Categorie)
admin.site.register(AiModel)