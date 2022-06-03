from django.shortcuts import get_object_or_404
# from django.db.models import Sum
from django.http import HttpResponse
# from django.db.models import QuerySet
from django.conf import settings
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from rest_framework.views import APIView

from app.serializers import (
    IngredientSerializer, TagSerializer, RecipeSerializer,
    RecipeCreateSerializer, FavoriteCreateSerializer,
    ShoppingCartCreateSerializer
)
from app.filters import IngredientFilter, RecipeFilter
from app.models import (
    Ingredient, Tag, Recipe, Favorite, ShoppingCart, RecipeIngredient
)
from app.paginations import LimitResultsSetPagination


class IngredientViewset(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet):

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filterset_class = IngredientFilter
    pagination_class = None


class TagViewset(mixins.ListModelMixin,
                 mixins.RetrieveModelMixin,
                 viewsets.GenericViewSet):

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class RecipeViewset(viewsets.ModelViewSet):

    serializer_class = RecipeSerializer
    pagination_class = LimitResultsSetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeSerializer
        return RecipeCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        serializer = RecipeSerializer(
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
        serializer = RecipeSerializer(
            instance=serializer.instance,
            context={'request': self.request},
        )
        return Response(
            serializer.data, status=status.HTTP_200_OK
        )

    def get_queryset(self):
        queryset = Recipe.objects.all()
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

    serializer_class = FavoriteCreateSerializer

    def create(self, request, *args, **kwargs):
        recipe = get_object_or_404(
            Recipe, id=self.kwargs.get('recipe_id')
        )
        user = self.request.user
        in_favorite = Favorite.objects.filter(
            user=user, recipe=recipe).exists()
        if in_favorite:
            content = {'error': f'{recipe.name} уже добавлен в избранное!'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        recipe = get_object_or_404(
            Recipe, id=self.kwargs.get('recipe_id')
        )
        serializer.save(user=self.request.user, recipe=recipe)

    @action(methods=['delete'], detail=False)
    def delete(self, request, *args, **kwargs):
        instance = get_object_or_404(
            Favorite,
            recipe=self.kwargs.get('recipe_id'),
            user=request.user.id
        )
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ShoppingCartViewset(mixins.CreateModelMixin,
                          mixins.DestroyModelMixin,
                          viewsets.GenericViewSet):

    serializer_class = ShoppingCartCreateSerializer

    def create(self, request, *args, **kwargs):
        recipe = get_object_or_404(
            Recipe, id=self.kwargs.get('recipe_id')
        )
        user = self.request.user
        in_shopping_cart = ShoppingCart.objects.filter(
            user=user, recipe=recipe).exists()
        if in_shopping_cart:
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
            Recipe, id=self.kwargs.get('recipe_id')
        )
        serializer.save(user=self.request.user, recipe=recipe)

    @action(methods=['delete'], detail=False)
    def delete(self, request, *args, **kwargs):
        instance = get_object_or_404(
            ShoppingCart,
            recipe=self.kwargs.get('recipe_id'),
            user=request.user.id
        )
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class DownloadShoppingCart(APIView):

    permission_classes = (IsAuthenticated,)

    # def _create_shopping_list(self, queryset: QuerySet,
    #                           response: HttpResponse) -> HttpResponse:
    #     """Формирует список продуктов и записывает его в
    #     переданный response.
    #     """
    #     unique_ingredient = []
    #     response.write('Список продуктов:\n')
    #     for item in queryset:
    #         recipe_ingredient = RecipeIngredient.objects.filter(
    #             recipe=item.recipe
    #         ).aggregate(total_amount=Sum('amount'))
    #         for row in recipe_ingredient:
    #             if row.ingredient.id not in unique_ingredient:
    #                 response.write(f'\n{row.ingredient._get_name()}')
    #                 response.write(f' - {item.total_amount}')
    #                 unique_ingredient.append(row.ingredient.id)
    #     return response

    def _create_shopping_list(self, queryset, response):
        ingredients_and_amount = {}
        response.write('Список продуктов:\n')
        for item in queryset:
            ingredients_recipe = RecipeIngredient.objects.filter(
                recipe=item.recipe
            )
            for row in ingredients_recipe:
                ingredient = row.ingredient
                amount = row.amount
                if ingredient in ingredients_and_amount:
                    if isinstance(ingredients_and_amount[ingredient], list):
                        ingredients_and_amount[ingredient].append(amount)
                    else:
                        ingredients_and_amount[ingredient] = [
                            ingredients_and_amount[ingredient], amount
                        ]
                else:
                    ingredients_and_amount[ingredient] = amount
        for ingredient, amount in ingredients_and_amount.items():
            response.write(f'\n{ingredient.name}')
            response.write((f' ({ingredient.measurement_unit})'))
            response.write(f' - {amount}')
        return response

    def get(self, request):
        """Формирует HttpResponse и передает ответ в виде файла
        списка покупок для юзера, который инициировал запрос.
        """
        response = HttpResponse(content_type='text/plain')
        response['Content-Disposition'] = (
            f'attachment; filename="{settings.SHOPPING_LIST_NAME}"'
        )
        return self._create_shopping_list(self.get_queryset(), response)

    def get_queryset(self):
        """Получает queryset списка покупок для юзера, который
        инициировал запрос.
        """
        user = self.request.user
        return user.shopping_cart.all()
