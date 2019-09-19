from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType

from apps.users.models import Organization, User
from apps.events.models import Event
from apps.locations.serializers import ShortPlaceSerializer, AddressSerializer
from apps.users.serializers import ShortUserSerializer, ShortOrganizationSerializer


class EventSerializer(serializers.ModelSerializer):
    """
    Serializer of Event model
    """
    organizer = serializers.SerializerMethodField(read_only=True)
    organizer_type = serializers.SerializerMethodField(read_only=True)
    place = ShortPlaceSerializer(required=False)
    address = AddressSerializer(required=False)

    class Meta:
        model = Event
        fields = '__all__'
        extra_kwargs = {'id': {'read_only': True},
                        'created': {'read_only': True},
                        'updated': {'read_only': True}
                        }

    def get_organizer(self, obj=None):
        """
        Method to fill out the organizer field in serializer
        """
        organizer_type_mapping = {
            ContentType.objects.get_for_model(User): ShortUserSerializer,
            ContentType.objects.get_for_model(Organization): ShortOrganizationSerializer
        }
        serializer_class = organizer_type_mapping.get(obj.organizer_type)
        return serializer_class(obj.organizer).data

    def get_organizer_type(self, obj=None):
        """
        Method to fill out the organizer type in serializer
        It converts model's number into models name
        """
        return obj.organizer.__class__.__name__
