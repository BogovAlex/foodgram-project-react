from rest_framework import viewsets, mixins
from djoser.views import UserViewSet as DjoserUserViewset

from users import models, serializers
from users.pagination import LimitResultsSetPagination


class UserViewSet(DjoserUserViewset):
    pagination_class = LimitResultsSetPagination

    def list(self, request):
        queryset = models.User.objects.all()
        page = self.paginate_queryset(queryset)
        serializer = serializers.AuthorSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)


class SubscriptionViewset(mixins.ListModelMixin,
                          mixins.RetrieveModelMixin,
                          viewsets.GenericViewSet):

    serializer_class = serializers.SubscriptionSerializer

    def get_queryset(self):
        user = self.request.user
        return models.Follow.objects.filter(user=user)
