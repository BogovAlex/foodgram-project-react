from rest_framework import viewsets, mixins

from app.serializers import IngredientSerializer
from app.models import Ingredient
from app.filters import IngredientFilter


class IngredientViewset(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet):

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filterset_class = IngredientFilter
