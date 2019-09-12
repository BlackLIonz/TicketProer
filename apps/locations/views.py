from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser

from apps.locations.models import Place, Address
from apps.locations.serializers import PlaceSerializer, AddressSerializer
from tools.action_based_permission import ActionBasedPermission


class PlaceViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A ViewSet for listing and retrieving Places
    """
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer


class AddressViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides `create()`, `retrieve()`, `update()`,
    `partial_update()`, `destroy()` and `list()` actions.
    """
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = (ActionBasedPermission,)
    action_permissions = {
        AllowAny: ['retrieve', 'list'],
        IsAuthenticated: ['create', 'update', 'partial_update'],
        IsAdminUser: ['destroy']
    }

    def perform_update(self, serializer):
        if self.request.user is not serializer.created_by:
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer.save()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
