from django.urls import path, include
from rest_framework.routers import SimpleRouter

from app import views

app_name = 'app'

approuter = SimpleRouter()
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
approuter.register(
    r'recipes/(?P<recipe_id>\d+)/favorite',
    views.FavoriteViewset, basename='favorite'
)
approuter.register(
    r'recipes/(?P<recipe_id>\d+)/shopping_cart',
    views.ShoppingCartViewset, basename='add_shopping_cart'
)


urlpatterns = [
    path(
        'recipes/download_shopping_cart/',
        views.DownloadShoppingCart.as_view()
    ),
    path('', include(approuter.urls))
]
