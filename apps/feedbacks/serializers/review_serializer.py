from django.contrib.contenttypes.models import ContentType
from django.db import models
from rest_framework import serializers

from apps.events.models import Event
from apps.events.serializers import EventSerializer
from apps.feedbacks.models.review import Review
from apps.locations.models import Place
from apps.locations.serializers import PlaceSerializer
from apps.users.models import Organization
from apps.users.serializers import UserSerializer, OrganizationSerializer


class ReviewSerializer(serializers.ModelSerializer):
    parent_object_type = serializers.SerializerMethodField()
    parent_object = serializers.SerializerMethodField()
    created_by = UserSerializer(required=False)

    parent_object_type_mapping = {
        Place: PlaceSerializer,
        Event: EventSerializer,
        Organization: OrganizationSerializer,
    }

    class Meta:
        model = Review
        fields = '__all__'
        extra_kwargs = {
            'id': {'read_only': True},
            'created': {'read_only': True},
            'updated': {'read_only': True},
            'created_by': {'read_only': True},
            'parent_object': {'read_only': True},
            'status': {'read_only': True},
        }

    def get_parent_object(self, obj=None):
        """
        Method to fill out the organizer field in serializer
        """
        serializer_class = self.parent_object_type_mapping.get(type(obj.parent_object))
        data = serializer_class(obj.parent_object).data
        return data

    def get_parent_object_type(self, obj=None):
        """
        Method to fill out the parent object type in serializer
        It converts model's number into models name
        """
        return obj.parent_object.__class__.__name__
