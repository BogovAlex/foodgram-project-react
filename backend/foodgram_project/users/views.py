from rest_framework import viewsets, mixins

from users import models, serializers


class SubscriptionViewset(mixins.ListModelMixin,
                          mixins.RetrieveModelMixin,
                          viewsets.GenericViewSet):

    queryset = models.Follow.objects.all()
    serializer_class = serializers.SubscriptionSerializer
