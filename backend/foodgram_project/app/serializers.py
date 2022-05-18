from rest_framework import serializers

from app.models import (
    Favorite, Ingredient, Tag, Recipe, RecipeIngredientAmount,
    ShoppingCart,
)
from users.serializers import AuthorSerializer


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class RecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.StringRelatedField(
        source='ingredient.id',
        read_only=True
    )
    name = serializers.StringRelatedField(
        source='ingredient.name',
        read_only=True
    )
    measurement_unit = serializers.PrimaryKeyRelatedField(
        source='ingredient.measurement_unit',
        read_only=True
    )

    class Meta:
        model = RecipeIngredientAmount
        fields = ('id', 'name', 'measurement_unit', 'amount',)


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    ingredients = serializers.SerializerMethodField()
    author = AuthorSerializer()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients', 'is_favorited',
            'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time',
        )

    def get_ingredients(self, obj):
        queryset = RecipeIngredientAmount.objects.filter(recipe_id=obj.id)
        serializer = RecipeIngredientSerializer(queryset, many=True)
        return serializer.data

    def get_is_favorited(self, obj):
        recipe = obj.id
        request = self.context.get('request')
        if request is not None:
            user = request.user.id
            return Favorite.objects.filter(
                user_id=user, recipe_id=recipe
            ).exists()
        return False

    def get_is_in_shopping_cart(self, obj):
        recipe = obj.id
        request = self.context.get('request')
        if request is not None:
            user = request.user.id
            return ShoppingCart.objects.filter(
                user_id=user, recipe_id=recipe
            ).exists()
        return False


class FavoriteCreateSerializer(serializers.ModelSerializer):
    id = serializers.StringRelatedField(
        source='recipe.id',
        read_only=True
    )
    name = serializers.StringRelatedField(
        source='recipe.name',
        read_only=True
    )
    image = serializers.StringRelatedField(
        source='recipe.image',
        read_only=True
    )
    cooking_time = serializers.StringRelatedField(
        source='recipe.cooking_time',
        read_only=True
    )

    class Meta:
        model = Favorite
        fields = ('id', 'name', 'image', 'cooking_time',)
        read_only_fields = ('user', 'recipe',)


class ShoppingCartCreateSerializer(FavoriteCreateSerializer):
    class Meta:
        model = ShoppingCart
        fields = ('id', 'name', 'image', 'cooking_time',)
