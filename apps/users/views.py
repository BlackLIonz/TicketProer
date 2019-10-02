from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from drf_yasg.openapi import Response as SwgResponse

from apps.base.views import ReviewsMixin
from apps.events.models import Event
from apps.events.serializers import EventSerializer
from apps.subscriptions.serializers import SubscriptionSerializer
from apps.users.models import User, Organization
from apps.users.serializers import (UserSerializer,
                                    ShortOrganizationSerializer,
                                    OrganizationWithEventsSerializer,
                                    DetailedOrganizationWithMembersSerializer)
from tools.action_based_permission import ActionBasedPermission


@method_decorator(name='subscriptions', decorator=swagger_auto_schema(
    operation_summary="List method that lists all user's subscriptions.",
    operation_description="Lists all user's Subscriptions. This endpoint is reachable by staff only.",
    responses={
        '200': SwgResponse('Ok. List returned.', SubscriptionSerializer()),
        '403': 'Forbidden. Not a staff user.',
        '404': 'Not found. Bad User id.',
    }
    )
)
class UserDataForStaffViewSet(RetrieveModelMixin,
                              viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (ActionBasedPermission,)
    action_permissions = {
        IsAdminUser: ['retrieve', 'subscriptions']
    }

    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def subscriptions(self, request, pk=None):
        user = self.get_object()
        serializer = SubscriptionSerializer(user.subscriptions, many=True)
        return Response(serializer.data)


class UserEventsViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = EventSerializer

    def list(self, request, *args, **kwargs):
        response = request.user.events
        serializer = self.get_serializer(response, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        event = get_object_or_404(Event, id=kwargs.get('event_id'))
        serializer = self.get_serializer(event)
        return Response(serializer.data, status=HTTP_200_OK)


class OrganizationsViewSet(viewsets.ReadOnlyModelViewSet, ReviewsMixin):
    permission_classes = [IsAuthenticated]
    serializer_class = ShortOrganizationSerializer

    def retrieve(self, request, *args, **kwargs):
        organization = get_object_or_404(self.get_queryset(), id=kwargs.get('organization_id'))
        serializer = OrganizationWithEventsSerializer(organization)
        return Response(serializer.data, status=HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def detailed(self, request, organization_id):
        organization = get_object_or_404(self.get_queryset(), id=organization_id)
        serializer = DetailedOrganizationWithMembersSerializer(organization)
        return Response(serializer.data, status=HTTP_200_OK)

    def get_queryset(self):
        return Organization.objects.all()
