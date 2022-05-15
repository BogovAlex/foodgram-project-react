from rest_framework import serializers
from djoser.serializers import (
    UserCreateSerializer, TokenCreateSerializer
)

from users.models import User, Follow
from app.models import Recipe


def is_subscribed(self, obj):
    author = obj.id
    request = self.context.get('request')
    if request is not None:
        user = request.user.id
        return Follow.objects.filter(user=user, author=author).exists()
    return False


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
        return is_subscribed(self, obj)


class SubscriptionRecipeSerializer(serializers.ModelSerializer):
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
    is_subscribed = serializers.SerializerMethodField()
    recipes = SubscriptionRecipeSerializer(
        many=True, source='author.recipe', required=False
    )
    recipes_count = serializers.ReadOnlyField(source='author.recipe.count')

    class Meta:
        model = Follow
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed', 'recipes', 'recipes_count',
        )

    def get_is_subscribed(self, obj):
        return is_subscribed(self, obj)
