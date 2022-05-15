from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

from app import models, filters, serializers
from app.paginations import LimitResultsSetPagination


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


class RecipeViewset(viewsets.ModelViewSet):

    queryset = models.Recipe.objects.all()
    serializer_class = serializers.RecipeSerializer
    pagination_class = LimitResultsSetPagination


class FavoriteViewset(mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    serializer_class = serializers.FavoriteCreateSerializer

    def perform_create(self, serializer):
        recipe = get_object_or_404(
            models.Recipe, id=self.kwargs.get('recipe_id')
        )
        serializer.save(user=self.request.user, recipe=recipe)

    @action(methods=['delete'], detail=False)
    def delete(self, request, *args, **kwargs):
        instance = get_object_or_404(
            models.Favorite,
            recipe=self.kwargs.get('recipe_id'),
            user=request.user.id
        )
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
