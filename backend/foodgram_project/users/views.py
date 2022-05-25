from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from djoser.views import UserViewSet as DjoserUserViewset
from django.shortcuts import get_object_or_404

from users import models, serializers
from users.paginations import LimitResultsSetPagination


class UserViewSet(DjoserUserViewset):
    pagination_class = LimitResultsSetPagination

    def list(self, request):
        queryset = models.User.objects.all()
        page = self.paginate_queryset(queryset)
        serializer = serializers.UserSerializer(
            page, many=True, context={'request': request}
        )
        return self.get_paginated_response(serializer.data)


class SubscriptionViewset(mixins.ListModelMixin,
                          mixins.RetrieveModelMixin,
                          viewsets.GenericViewSet):

    serializer_class = serializers.SubscriptionSerializer
    pagination_class = LimitResultsSetPagination
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return models.Follow.objects.filter(user=user)


class SubscriptionCreateDestroy(mixins.CreateModelMixin,
                                mixins.DestroyModelMixin,
                                viewsets.GenericViewSet):

    serializer_class = serializers.SubscriptionSerializer
    permission_classes = (IsAuthenticated,)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["author"] = int(self.kwargs.get('author_id'))
        return context

    def perform_create(self, serializer):
        author = get_object_or_404(
            models.User,
            id=self.kwargs.get('author_id')
        )
        serializer.save(user=self.request.user, author=author)

    @action(methods=['delete'], detail=False)
    def delete(self, request, *args, **kwargs):
        instance = get_object_or_404(
            models.Follow,
            author=self.kwargs.get('author_id'),
            user=request.user.id
        )
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
