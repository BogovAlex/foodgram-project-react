from django.urls import path, include
from rest_framework.routers import DefaultRouter

from app import views

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


urlpatterns = [
    # path('users/', include('users.urls')),
    path('', include(approuter.urls))
]
