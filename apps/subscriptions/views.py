from rest_framework import filters as rest_filters, viewsets
from django_filters import rest_framework as filters
from rest_framework.permissions import IsAuthenticated


from apps.subscriptions.models import Subscription
from apps.subscriptions.serializers import SubscriptionSerializer


class SubscriptionFilter(filters.FilterSet):
    event__date__gte = filters.DateTimeFilter(field_name='event__date', lookup_expr="gte")
    event__date__lte = filters.DateTimeFilter(field_name='event__date', lookup_expr="lte")

    class Meta:
        model = Subscription
        fields = ['user', 'event', 'status', 'event__date__lte', 'event__date__gte']


class SubscriptionViewSet(viewsets.ReadOnlyModelViewSet):

    model = Subscription
    serializer_class = SubscriptionSerializer
    filter_backends = [filters.DjangoFilterBackend, rest_filters.OrderingFilter]
    filterset_class = SubscriptionFilter

    ordering_fields = ('event__date',)
    ordering = ('event__date',)

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.all_active_subscriptions
