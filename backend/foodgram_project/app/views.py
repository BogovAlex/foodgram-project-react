from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.http import Http404, HttpResponse
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

    serializer_class = serializers.RecipeSerializer
    pagination_class = LimitResultsSetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = filters.RecipeFilter

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return serializers.RecipeSerializer
        return serializers.RecipeCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        serializer = serializers.RecipeSerializer(
            instance=serializer.instance,
            context={'request': self.request}
        )
        return Response(
            serializer.data, status=status.HTTP_201_CREATED
        )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=False
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        serializer = serializers.RecipeSerializer(
            instance=serializer.instance,
            context={'request': self.request},
        )
        return Response(
            serializer.data, status=status.HTTP_200_OK
        )

    def get_queryset(self):
        queryset = models.Recipe.objects.all()
        user = self.request.user
        is_favorited = self.request.query_params.get('is_favorited')
        is_in_shopping_cart = (
            self.request.query_params.get('is_in_shopping_cart')
        )

        if is_favorited == '1':
            queryset = queryset.filter(favorite__user=user)
        if is_in_shopping_cart == '1':
            queryset = queryset.filter(shopping_cart__user=user)

        return queryset


class FavoriteViewset(mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):

    serializer_class = serializers.FavoriteCreateSerializer

    def create(self, request, *args, **kwargs):
        recipe = get_object_or_404(
            models.Recipe, id=self.kwargs.get('recipe_id')
        )
        user = self.request.user
        already_favorite = models.Favorite.objects.filter(
            user=user, recipe=recipe).exists()
        if already_favorite:
            content = {'error': f'{recipe.name} уже добавлен в избранное!'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

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

    def create(self, request, *args, **kwargs):
        recipe = get_object_or_404(
            models.Recipe, id=self.kwargs.get('recipe_id')
        )
        user = self.request.user
        already_favorite = models.ShoppingCart.objects.filter(
            user=user, recipe=recipe).exists()
        if already_favorite:
            content = {
                'error': f'{recipe.name} уже добавлен в корзину покупок!'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

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


class DownloadShoppingCart(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        ingredients = {}
        for item in self.get_queryset():
            value = models.RecipeIngredient.objects.filter(
                recipe=item.recipe
            )
            for val in value:
                if val.ingredient.__str__() in ingredients.keys():
                    qnt = ingredients[val.ingredient.__str__()]
                    ingredients[val.ingredient.__str__()] = qnt + val.amount
                else:
                    ingredients[val.ingredient.__str__()] = val.amount
        with open('shopping_list.txt', 'w') as f:
            f.write('Список покупок:\n')
            for ingredient, qnt in ingredients.items():
                f.write('\n{} - {}'.format(ingredient, qnt))
            f.close()
        with open('shopping_list.txt', 'r') as f:
            file_data = f.read()
            f.close()
        response = HttpResponse(file_data, content_type='text/plain')
        response['Content-Disposition'] = (
            'attachment; filename="shopping-list.txt"'
        )
        return response

    def get_queryset(self):
        user = self.request.user
        return models.ShoppingCart.objects.filter(user=user)
