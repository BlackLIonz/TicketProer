from rest_framework import serializers

from apps.locations.models.place import Place
from apps.locations.serializers.address_serializer import AddressSerializer


class PlaceSerializer(serializers.ModelSerializer):
    address = AddressSerializer(required=False)

    class Meta:
        model = Place
        fields = '__all__'
        extra_kwargs = {
            'id': {'read_only': True},
            'created': {'read_only': True},
            'updated': {'read_only': True},
            'status': {'read_only': True},
        }


class ShortPlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        exclude = ['address', 'updated']
        extra_kwargs = {'id': {'read_only': True},
                        'created': {'read_only': True},
                        'status': {'read_only': True},
                        }
