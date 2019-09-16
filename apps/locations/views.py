from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response

from apps.locations.models import Place, Address
from apps.locations.serializers import PlaceSerializer, AddressSerializer
from tools.action_based_permission import ActionBasedPermission


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

    def create(self, request, *args, **kwargs):
        data_dict = request.data.dict()
        data = data_dict.pop('address')
        if data is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        address_ser = AddressSerializer(data=data)
        address_ser.is_valid()
        address = Address.objects.create(**address_ser.validated_data)
        serializer = self.get_serializer(data=data_dict)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer, address=address)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer, **kwargs):
        Place.objects.create(**kwargs, **serializer.validated_data)
