from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend

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
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('tags', 'author',)

    def list(self, request):
        queryset = models.Recipe.objects.all()
        user = request.user
        is_favorited = self.request.query_params.get('is_favorited')
        is_in_shopping_cart = (
            self.request.query_params.get('is_in_shopping_cart')
        )
        if is_favorited == '1':
            queryset = queryset.filter(favorite__user=user)
        if is_in_shopping_cart == '1':
            queryset = queryset.filter(shopping_cart__user=user)
        page = self.paginate_queryset(queryset)
        serializer = serializers.RecipeSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)


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
        try:
            instance = get_object_or_404(
                models.Favorite,
                recipe=self.kwargs.get('recipe_id'),
                user=request.user.id
            )
        except Http404 as error:
            content = {'error': str(error)}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ShoppingCartViewset(mixins.CreateModelMixin,
                          mixins.DestroyModelMixin,
                          viewsets.GenericViewSet):

    serializer_class = serializers.ShoppingCartCreateSerializer

    def perform_create(self, serializer):
        recipe = get_object_or_404(
            models.Recipe, id=self.kwargs.get('recipe_id')
        )
        serializer.save(user=self.request.user, recipe=recipe)

    @action(methods=['delete'], detail=False)
    def delete(self, request, *args, **kwargs):
        try:
            instance = get_object_or_404(
                models.ShoppingCart,
                recipe=self.kwargs.get('recipe_id'),
                user=request.user.id
            )
        except Http404 as error:
            content = {'error': str(error)}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
