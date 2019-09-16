from rest_framework import serializers

from apps.locations.models import Address


class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = '__all__'
        extra_kwargs = {
            'id': {'read_only': True},
            'created': {'read_only': True},
            'updated': {'read_only': True},
            'created_by': {'read_only': True},
        }
