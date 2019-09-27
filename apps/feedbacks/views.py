import uuid

from django.contrib.contenttypes.models import ContentType
from django_filters import rest_framework as filters
from rest_framework import filters as rest_filters
from rest_framework import viewsets, status, exceptions
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from apps.events.models import Event
from apps.feedbacks.models import Comment, Review
from apps.feedbacks.serializers import ReviewSerializer
from apps.feedbacks.serializers.comment_serializer import CommentSerializer
from apps.locations.models import Place
from apps.users.models import Organization
from tools.action_based_permission import ActionBasedPermission
from tools.custom_permissions import IsOwnerOrAdmin, IsOwner
from tools.custom_permissions import IsVisited
from tools.shortcuts import get_object_or_None


class RatingFilter(filters.FilterSet):
    rating_gte = filters.NumberFilter(field_name='rating', lookup_expr='gte')
    rating_lte = filters.NumberFilter(field_name='rating', lookup_expr='lte')

    class Meta:
        model = Review
        fields = ['rating_gte', 'rating_lte']


class ReviewViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides default `create()`, `retrieve()`, `update()`,
    `partial_update()`, `destroy()` and `list()` actions.
   """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (ActionBasedPermission,)
    action_permissions = {
        AllowAny: ['retrieve', 'list'],
        IsVisited: ['create'],
        IsOwnerOrAdmin: ['destroy', 'update', 'partial_update'],
    }
    filter_backends = [filters.DjangoFilterBackend, rest_filters.OrderingFilter]
    filterset_class = RatingFilter

    def get_queryset(self):
        if self.request.user.is_staff:
            return Review.objects.all()
        else:
            return Review.objects.filter(status__in=[Review.OK, Review.SUSPICIOUS])

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        if instance.status == Review.DELETED:
            raise exceptions.PermissionDenied('You can not create reviews on it')
        instance.status = Review.OK
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = Review.DELETED
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.save()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        user = request.user
        data = dict(request.data)
        parent_object = self._get_parent(data)
        if type(parent_object) is Event and not parent_object.is_available_for_feedback:
            raise exceptions.PermissionDenied('Event is not available for feedbacks')
        serializer_class = self.get_serializer_class()
        review = serializer_class(data=data)
        review.is_valid(raise_exception=True)
        review = self.perform_create(review,
                                     created_by=user,
                                     parent_object_id=parent_object.id,
                                     parent_object_type=ContentType.objects.get_for_model(type(parent_object)))
        review_data = serializer_class(review).data
        headers = self.get_success_headers(review_data)
        return Response(review_data, status=status.HTTP_201_CREATED, headers=headers)

    def _get_parent(self, data):
        parent_object_id = data.pop('parent_object')
        parent_object = (get_object_or_None(Place, pk=parent_object_id) or
                         get_object_or_None(Event, pk=parent_object_id) or
                         get_object_or_None(Organization, pk=parent_object_id))
        if parent_object is None:
            raise exceptions.NotFound('Place/Event/Organization not found')
        parent_object_type = ContentType.objects.get_for_model(parent_object.__class__)
        data['parent_object_id'] = parent_object_id
        data['parent_object_type'] = parent_object_type
        return parent_object

    def perform_create(self, serializer, **kwargs):
        review = Review.objects.filter(created_by=kwargs['created_by'], parent_object_id=kwargs['parent_object_id'])
        if review.exists():
            review = review.first()
            raise exceptions.APIException(detail=f'Review already exists, at {review.id}', code=status.HTTP_200_OK)
        else:
            return Review.objects.create(**kwargs, **serializer.validated_data)


class CommentViewSet(viewsets.ModelViewSet):
    """
    A viewset for Comment model, which provides
    `create()`, `retrieve()`, `update()`,
    `partial_update()`, `destroy()` and `list()` actions
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (ActionBasedPermission,)
    action_permissions = {
        AllowAny: ['retrieve', 'list'],
        IsAuthenticated: ['create'],
        IsOwner: ['update', 'partial_update'],
        IsOwnerOrAdmin: ['destroy'],
    }

    def list(self, request, *args, **kwargs):
        if request.user.is_staff:
            queryset = self.filter_queryset(self.get_queryset())
        else:
            queryset = self.filter_queryset(self.get_queryset().exclude(status=Comment.DELETED))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        user = request.user
        data_dict = request.data
        models_mapping = {
            Event.__name__: (Event, ContentType.objects.get_for_model(Event)),
            Organization.__name__: (Organization, ContentType.objects.get_for_model(Organization)),
            Place.__name__: (Place, ContentType.objects.get_for_model(Place)),
            Comment.__name__: (Comment, ContentType.objects.get_for_model(Comment)),
            Review.__name__: (Review, ContentType.objects.get_for_model(Review)),
        }
        self.validate_data(data_dict)
        topic_id, topic_type = self.get_topic_or_parent(data_dict, models_mapping, 'topic')
        parent_id, parent_type = self.get_topic_or_parent(data_dict, models_mapping, 'parent')
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=data_dict)
        serializer.is_valid(raise_exception=True)
        comment = self.perform_create(serializer, created_by=user, topic_type=topic_type,
                                      topic_id=topic_id, parent_type=parent_type, parent_id=parent_id)
        comment_data = serializer_class(comment).data
        headers = self.get_success_headers(comment_data)
        return Response(comment_data, status=status.HTTP_201_CREATED, headers=headers)

    def validate_data(self, data_dict):
        for item in ('topic', 'topic_type', 'parent', 'parent_type'):
            if item not in data_dict:
                raise exceptions.ParseError('Please, transmit topic and parent')

    def get_topic_or_parent(self, data_dict, models_mapping, obj_class):
        obj_from_user = data_dict.pop(obj_class)
        obj_type_from_user = data_dict.pop(f'{obj_class}_type').title()
        obj_model, obj_type = models_mapping.get(obj_type_from_user)
        obj = self.get_created_object(obj_from_user.get('id'), obj_model)
        if obj_class == 'parent':
            self.check_parent_status(obj)
        obj_id = obj.id
        return obj_id, obj_type

    def check_parent_status(self, obj):
        if hasattr(obj, 'status') and isinstance(obj.status, str) and obj.status.lower() == 'deleted':
            raise exceptions.ParseError('Parent object does not exist')

    def get_created_object(self, obj_id, cls):
        """Validates ID"""
        try:
            return cls.objects.get(id=uuid.UUID(str(obj_id)))
        except ValueError:
            raise exceptions.ParseError(f'{cls.__name__}\'s ID is not valid')
        except cls.DoesNotExist:
            raise exceptions.NotFound('No such ID in database')

    def perform_create(self, serializer, **kwargs):
        return Comment.objects.create(**kwargs, **serializer.validated_data)

    def perform_destroy(self, instance):
        instance.status = Comment.DELETED
        instance.save()
