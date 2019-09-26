from django.contrib.contenttypes.models import ContentType
from django_filters import rest_framework as filters
from rest_framework import viewsets, status, exceptions, filters as rest_filters
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from apps.events.models import Event
from apps.feedbacks.models import Review
from apps.feedbacks.serializers import ReviewSerializer
from apps.locations.models import Place
from apps.users.models import Organization
from tools.action_based_permission import ActionBasedPermission
from tools.custom_permissions import IsOwnerOrAdmin
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
        IsAuthenticated: ['create'],  # will changed on IsVisited
        IsOwnerOrAdmin: ['destroy', 'update', 'partial_update'],
    }
    filter_backends = [filters.DjangoFilterBackend, rest_filters.OrderingFilter]
    filterset_class = RatingFilter

    def create(self, request, *args, **kwargs):
        user = request.user
        data = dict(request.data)
        parent_object = self._get_parent(data)
        if type(parent_object) is Event and not parent_object.is_available_for_feedback:
            raise exceptions.PermissionDenied('Event is not available for feedbacks')
        serializer_class = self.get_serializer_class()
        review = serializer_class(data=data)
        review.is_valid(raise_exception=True)
        review = self.perform_create(review, created_by=user, parent_object=parent_object)
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
        data['parent_object_it'] = parent_object_id
        data['parent_object_type'] = parent_object_type
        return parent_object

    def perform_create(self, serializer, **kwargs):
        return Review.objects.create(**kwargs, **serializer.validated_data)
