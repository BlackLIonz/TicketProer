from django.contrib.contenttypes.models import ContentType
from django.shortcuts import _get_queryset
from rest_framework import viewsets, status, exceptions
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from apps.events.models import Event
from apps.feedbacks.serializers import ReviewSerializer
from apps.feedbacks.models import Review
from apps.locations.models import Place
from apps.users.models import Organization
from tools.action_based_permission import ActionBasedPermission
from tools.custom_permissions import IsOwnerOrAdmin
from tools.shortcuts import get_object_or_None


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

    def create(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        parent_object = self.get_parent(data)
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer, created_by=user, parent_object=parent_object)
        # headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_parent(self, data):
        parent_object_id = data.pop('parent_object')
        parent_object = (get_object_or_None(Place, pk=parent_object_id) or
                         get_object_or_None(Event, pk=parent_object_id) or
                         get_object_or_None(Organization, pk=parent_object_id))
        parent_object_type = ContentType.objects.get_for_model(parent_object.__class__)
        data['parent_object_it'] = parent_object_id
        data['parent_object_type'] = parent_object_type
        return parent_object

    def perform_create(self, serializer, **kwargs):
        return Review.objects.create(**kwargs, **serializer.validated_data)
