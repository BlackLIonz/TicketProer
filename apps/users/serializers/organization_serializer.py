from rest_framework import serializers
from apps.users.models import Organization


class OrganizationSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    name = serializers.CharField(max_length=150, allow_blank=False, allow_null=False)
    email = serializers.EmailField(required=True, allow_blank=False, allow_null=False)
    profile_image = serializers.ImageField(allow_empty_file=True, allow_null=True)
    description = serializers.CharField(allow_blank=True, allow_null=True)
    approved = serializers.BooleanField(default=False)


class ShortOrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ['name', 'email']
