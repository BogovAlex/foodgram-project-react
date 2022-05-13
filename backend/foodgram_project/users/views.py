from rest_framework import viewsets, mixins

from users import models, serializers


class SubscriptionViewset(mixins.ListModelMixin,
                          mixins.RetrieveModelMixin,
                          viewsets.GenericViewSet):

    serializer_class = serializers.SubscriptionSerializer

    def get_queryset(self):
        user = self.request.user
        return models.Follow.objects.filter(user=user)
