from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAdminUser

from apps.locations.models import Place
from tools.action_based_permission import ActionBasedPermission
from apps.locations.serializers import PlaceSerializer


class PlaceViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for listing and retrieving Places
    """
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    permission_classes = (ActionBasedPermission,)
    action_permissions = {
        AllowAny: ['retrieve', 'list'],
        IsAdminUser: ['destroy', 'create', 'update', 'partial_update'],
    }
