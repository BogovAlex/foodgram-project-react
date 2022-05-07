from rest_framework import viewsets, mixins

from app import models, filters, serializers


class IngredientViewset(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet):

    queryset = models.Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer
    filterset_class = filters.IngredientFilter
    pagination_class = None


class TagViewset(mixins.ListModelMixin,
                 mixins.RetrieveModelMixin,
                 viewsets.GenericViewSet):

    queryset = models.Tag.objects.all()
    serializer_class = serializers.TagSerializer
    pagination_class = None
