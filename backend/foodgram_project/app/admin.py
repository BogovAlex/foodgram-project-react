from django.contrib import admin

from app import models


class TagInline(admin.StackedInline):
    model = models.TagsRecipe
    extra = 1


class IngredientInline(admin.StackedInline):
    model = models.RecipeIngredient
    extra = 1


@admin.register(models.Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit',)
    search_fields = ('name',)
    list_filter = ('measurement_unit',)


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug',)
    search_fields = ('name', 'color', 'slug')
    list_filter = ('name',)


@admin.register(models.Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = (TagInline, IngredientInline,)

    list_display = (
        'name', 'author',
    )
    list_filter = ('author', 'name', 'tags',)
    exclude = ('tags',)


@admin.register(models.Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'recipe',
    )
    list_filter = ('user',)


@admin.register(models.ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'recipe',
    )
    list_filter = ('user',)
