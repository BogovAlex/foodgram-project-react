from django.contrib import admin

from app import models


@admin.register(models.Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ['name', 'measurement_unit']
    search_fields = ('name',)
    list_filter = ('measurement_unit',)


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'color', 'slug']
    search_fields = ('name', 'color', 'slug')
    list_filter = ('name',)
