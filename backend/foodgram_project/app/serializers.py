from rest_framework import serializers
from django.shortcuts import get_object_or_404
from django.http import Http404

from app.models import (
    Favorite, Ingredient, Tag, Recipe, RecipeIngredient,
    ShoppingCart, TagsRecipe,
)
from app.fields import Base64ImageField
from users.serializers import UserSerializer


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class RecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.StringRelatedField(source='ingredient.id')
    name = serializers.StringRelatedField(source='ingredient.name')
    measurement_unit = serializers.StringRelatedField(
        source='ingredient.measurement_unit'
    )
    amount = serializers.IntegerField()

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    author = UserSerializer(read_only=True)
    ingredients = RecipeIngredientSerializer(
        source='ingredient',
        many=True,
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField(required=True)

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients', 'is_favorited',
            'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time',
        )

    def create(self, validated_data):
        tags = self.initial_data.pop('tags')
        ingredients = self.initial_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        for tag in tags:
            try:
                current_tag = get_object_or_404(
                    Tag, id=tag
                )
            except Http404:
                raise serializers.ValidationError(f'ID:{tag} не существует!')
            # TagsRecipe.objects.create(recipe=recipe, tag=current_tag)
        return recipe

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
