from rest_framework import serializers
from apps.locations.models import Address


class AddressSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    country = serializers.CharField(max_length=30, allow_blank=False, allow_null=False)
    city = serializers.CharField(max_length=30, allow_blank=False, allow_null=False)
    street = serializers.CharField(max_length=30, allow_blank=True, allow_null=True)
    house = serializers.CharField(max_length=10, allow_blank=True, allow_null=True)
    floor = serializers.IntegerField(min_value=0, allow_null=True)
    apartments = serializers.CharField(max_length=10, allow_blank=True, allow_null=True)
    descriptions = serializers.CharField(max_length=200, allow_blank=True, allow_null=True)




