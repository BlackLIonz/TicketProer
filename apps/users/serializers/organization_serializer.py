from rest_framework import serializers

from apps.users.models import Organization


class OrganizationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Organization
        fields = '__all__'
        extra_kwargs = {'id': {'read_only': True},
                        'created': {'read_only': True},
                        'updated': {'read_only': True},
                        'approved': {'read_only': True},
                        }


class ShortOrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ['id', 'name', 'email']
        extra_kwargs = {'id': {'read_only': True}}
