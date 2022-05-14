from rest_framework import serializers
from djoser.serializers import (
    UserCreateSerializer, TokenCreateSerializer
)

from users.models import User, Follow
from app.models import Recipe


class UserRegistrationSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        fields = (
            'email', 'username', 'first_name',
            'last_name', 'password',
        )


class TokenRegistrationSerializer(TokenCreateSerializer):
    class Meta:
        fields = ('password', 'email',)


class AuthorSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed',
        )

    def get_is_subscribed(self, obj):
        author = obj.id
        request = self.context.get("request")
        if request:
            user = request.user.id
            return Follow.objects.filter(user=user, author=author).exists()
        return False


class SubRecipes(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time',)


class SubscriptionSerializer(serializers.ModelSerializer):
    email = serializers.StringRelatedField(
        source='author.email',
        read_only=True
    )
    id = serializers.StringRelatedField(
        source='author.id',
        read_only=True
    )
    username = serializers.StringRelatedField(
        source='author.username',
        read_only=True
    )
    first_name = serializers.StringRelatedField(
        source='author.first_name',
        read_only=True
    )
    last_name = serializers.StringRelatedField(
        source='author.last_name',
        read_only=True
    )
    recipes = SubRecipes(many=True, source='author.recipe')
    recipes_count = serializers.ReadOnlyField(source='author.recipe.count')

    class Meta:
        model = Follow
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name', 'recipes',
            'recipes_count'
        )
