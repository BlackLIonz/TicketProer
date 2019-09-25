from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView


from apps.events.models import Event
from apps.events.serializers import EventSerializer
from apps.subscriptions.serializers import SubscriptionSerializer
from tools.action_based_permission import ActionBasedPermission
from apps.users.models import User, Organization
from apps.users.serializers import UserSerializer, ShortOrganizationSerializer
from apps.users.serializers.organization_serializer import (OrganizationWithEventsSerializer,
                                                            DetailedOrganizationWithMembersSerializer)


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

    def list(self, request, *args, **kwargs):
        response = request.user.events
        serializer = EventSerializer(response, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        event = get_object_or_404(Event, id=kwargs.get('event_id'))
        serializer = EventSerializer(event)
        return Response(serializer.data, status=HTTP_200_OK)


class OrganizationsView(APIView):
    def get(self, request):
        organizations = self.get_queryset()
        serializer = ShortOrganizationSerializer(organizations, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

    def get_queryset(self):
        return Organization.objects.all()


class DetailsWithAllEventsOrganizationView(APIView):
    def get(self, request, organization_id):
        organization = get_object_or_404(self.get_queryset(), id=organization_id)
        serializer = OrganizationWithEventsSerializer(organization)
        return Response(serializer.data, status=HTTP_200_OK)

    def get_queryset(self):
        return Organization.objects.all()


class DetailedOrganizationView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, organization_id):
        organization = get_object_or_404(self.get_queryset(), id=organization_id)
        serializer = DetailedOrganizationWithMembersSerializer(organization)
        return Response(serializer.data, status=HTTP_200_OK)

    def get_queryset(self):
        return Organization.objects.all()
