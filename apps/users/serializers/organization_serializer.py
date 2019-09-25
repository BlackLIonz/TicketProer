from rest_framework import serializers

from apps.events.serializers import EventSerializer
from apps.users.models import Organization
from apps.users.serializers import UserSerializer


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


class OrganizationWithEventsSerializer(ShortOrganizationSerializer):
    events = EventSerializer(many=True, source='all_events')

    class Meta:
        model = Organization
        fields = ['id', 'name', 'email', 'events']
        extra_kwargs = {'id': {'read_only': True}}


class DetailedOrganizationWithMembersSerializer(OrganizationSerializer):
    members = UserSerializer(many=True, source='all_members')

    class Meta(OrganizationSerializer.Meta):
        pass
