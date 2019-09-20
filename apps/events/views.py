from django_filters import rest_framework as filters
from rest_framework import viewsets, filters as rest_filters

from apps.events.models import Event
from apps.events.serializers import EventSerializer
from apps.base.filters import AddressFilter, PlaceFilter, DateFilter


class EventFilter(PlaceFilter, AddressFilter, DateFilter):
    organizer = filters.UUIDFilter(field_name='organizer_id')
    is_top = filters.BooleanFilter(field_name='is_top')
    is_hot = filters.BooleanFilter(field_name='is_hot')

    class Meta:
        model = Event
        fields = ['place', 'address', 'organizer', 'date__lte', 'date__gte', 'is_top', 'is_hot']


class EventViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A ViewSet for listing and retrieving events
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filter_backends = [filters.DjangoFilterBackend, rest_filters.OrderingFilter]
    filterset_class = EventFilter
    ordering_fields = ('created',)
    ordering = ('created',)
