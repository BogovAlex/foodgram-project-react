import django_filters

from app.models import Ingredient, Recipe


class IngredientFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        field_name='name', lookup_expr='icontains'
    )

    class Meta():
        model = Ingredient
        fields = ('name',)


class RecipeFilter(django_filters.FilterSet):
    author = django_filters.CharFilter(field_name='author__id',)
    tags = django_filters.CharFilter(field_name='tags__slug',)

    class Meta:
        model = Recipe
        fields = ('author', 'tags',)
