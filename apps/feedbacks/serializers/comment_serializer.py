from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers

from apps.events.models import Event
from apps.events.serializers import EventSerializer
from apps.feedbacks.models import Comment, Review
from apps.feedbacks.serializers import ReviewSerializer
from apps.locations.models import Place
from apps.locations.serializers import ShortPlaceSerializer
from apps.users.models import Organization
from apps.users.serializers import ShortOrganizationSerializer


class ShortCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id']
        extra_kwargs = {'id': {'read_only': True}}


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for Comment model
    """
    topic_type = serializers.SerializerMethodField(read_only=True)
    topic = serializers.SerializerMethodField(read_only=True)
    parent_type = serializers.SerializerMethodField(read_only=True)
    parent = serializers.SerializerMethodField(read_only=True)

    object_type_mapping = {
        ContentType.objects.get_for_model(Organization): ShortOrganizationSerializer,
        ContentType.objects.get_for_model(Place): ShortPlaceSerializer,
        ContentType.objects.get_for_model(Event): EventSerializer,
        ContentType.objects.get_for_model(Comment): ShortCommentSerializer,
        ContentType.objects.get_for_model(Review): ReviewSerializer,
    }

    class Meta:
        model = Comment
        fields = '__all__'
        extra_kwargs = {'id': {'read_only': True},
                        'created': {'read_only': True},
                        'updated': {'read_only': True},
                        }

    def get_topic(self, obj=None):
        """
        Method to fill out the topic field in serializer
        """
        serializer_class = self.object_type_mapping.get(obj.topic_type)
        data = serializer_class(obj.topic).data
        return {"id": str(data.get('id'))}

    def get_topic_type(self, obj=None):
        """
        Method to fill out the topic type in serializer
        It converts model's number into models name
        """
        return obj.topic.__class__.__name__

    def get_parent(self, obj=None):
        """
        Method to fill out the parent field in serializer
        """
        serializer_class = self.object_type_mapping.get(obj.parent_type)
        data = serializer_class(obj.parent).data
        return {"id": str(data.get('id'))}

    def get_parent_type(self, obj=None):
        """
        Method to fill out the parent type in serializer
        It converts model's number into models name
        """
        return obj.parent.__class__.__name__
