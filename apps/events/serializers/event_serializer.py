from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType

from apps.users.models import Organization, User
from apps.events.models import Event

from apps.locations.serializers.place_serializer import ShortPlaceSerializer
from apps.locations.serializers.address_serializer import AddressSerializer
from apps.users.serializers import UserSerializer, OrganizationSerializer


class EventSerializer(serializers.ModelSerializer):
    """
    Serializer of Event model
    """
    id = serializers.UUIDField(read_only=True)
    name = serializers.CharField(required=True, max_length=64, allow_blank=False, allow_null=False)
    description = serializers.CharField(required=True, allow_blank=False, allow_null=False)
    poster = serializers.ImageField(required=False, allow_empty_file=True)
    organizer = serializers.SerializerMethodField(read_only=True)
    place = ShortPlaceSerializer()
    address = AddressSerializer()
    date = serializers.DateTimeField(required=True, allow_null=False)
    duration = serializers.DurationField(required=True, min_value=None, max_value=None, allow_null=False)
    age_rate = serializers.IntegerField(required=True, min_value=0, allow_null=False)
    max_members = serializers.IntegerField(required=True, min_value=0, allow_null=False)
    status = serializers.ChoiceField(choices=Event.STATUS_TYPES)

    class Meta:
        model = Event
        fields = '__all__'

    def get_organizer(self, obj=None):
        """
        Method to fill out the organizer field in serializer
        """
        organizer_type_mapping = {
            ContentType.objects.get_for_model(User): UserSerializer,
            ContentType.objects.get_for_model(Organization): OrganizationSerializer
        }
        serializer_class = organizer_type_mapping.get(obj.organizer_type)
        return serializer_class(obj.organizer).data

