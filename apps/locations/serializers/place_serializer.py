from rest_framework import serializers

from apps.locations.models.place import Place
from apps.locations.serializers.address_serializer import AddressSerializer


class PlaceSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    name = serializers.CharField(max_length=75, allow_blank=False, allow_null=False)
    address = AddressSerializer()
    photo = serializers.ImageField(required=False, allow_empty_file=True, allow_null=True)
    description = serializers.CharField(max_length=200, allow_blank=True, allow_null=True)
    status = serializers.ChoiceField(choices=Place.STATUS_CHOICES)


class ShortPlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        exclude = ['address', 'updated']
