from rest_framework import serializers
from djoser.serializers import (
    UserCreateSerializer, TokenCreateSerializer
)

from users.models import User, Follow


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
        user = request.user.id
        return Follow.objects.filter(user=user, author=author).exists()


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ('user', 'author',)
