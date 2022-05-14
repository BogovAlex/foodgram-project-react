from django.urls import path, include
from rest_framework.routers import DefaultRouter

from app import views

app_name = 'app'

approuter = DefaultRouter()
approuter.register(
    r'ingredients',
    views.IngredientViewset,
    basename='ingredients'
)
approuter.register(
    r'tags',
    views.TagViewset,
    basename='tags'
)
approuter.register(
    r'recipes',
    views.RecipeViewset,
    basename='recipes'
)


urlpatterns = [
    path('', include(approuter.urls)),
]
