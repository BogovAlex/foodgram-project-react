from django.urls import path, include
from rest_framework.routers import DefaultRouter

from app import views

router_v1 = DefaultRouter()
router_v1.register(
    r'ingredients',
    views.IngredientViewset,
    basename='ingredients'
)


urlpatterns = [
    path('', include(router_v1.urls))
]
