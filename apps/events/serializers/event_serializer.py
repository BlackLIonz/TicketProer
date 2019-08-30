from rest_framework import serializers
from generic_relations.relations import GenericRelatedField

from apps.users.models import Organization, User
from apps.events.models import Event

from apps.locations.serializers.place_serializer import PlaceSerializer
from apps.locations.serializers.address_serializer import AddressSerializer
from apps.users.serializers.user_serializer import UserSerializer
from apps.users.serializers.organization_serializer import OrganizationSerializer


class EventSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    name = serializers.CharField(required=True, max_length=64, allow_blank=False, allow_null=False)
    description = serializers.CharField(required=True, allow_blank=False, allow_null=False)
    poster = serializers.ImageField(required=False, allow_empty_file=True)
    organizer = GenericRelatedField({
        Organization: OrganizationSerializer(),
        User: UserSerializer()
    })
    place = PlaceSerializer()
    address = AddressSerializer()
    date = serializers.DateTimeField(required=True, allow_null=False)
    duration = serializers.DurationField(required=True, min_value=None, max_value=None, allow_null=False)
    age_rate = serializers.IntegerField(required=True, min_value=0, default=0, allow_null=False)
    max_members = serializers.IntegerField(required=True, min_value=0, default=0, allow_null=False)
    status = serializers.ChoiceField(choices=Event.STATUS_TYPES)
