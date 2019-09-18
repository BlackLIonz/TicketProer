import json

from rest_framework import viewsets, status, exceptions
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
        data_dict = request.data
        data = data_dict.pop('address')
        if data is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        address_ser = AddressSerializer(data=data)
        address_ser.is_valid()
        address = Address.objects.create(**address_ser.validated_data)
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=data_dict)
        serializer.is_valid(raise_exception=True)
        place = self.perform_create(serializer, address=address)
        place_data = serializer_class(place).data
        headers = self.get_success_headers(serializer.data)
        return Response(place_data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer, **kwargs):
        return Place.objects.create(**kwargs, **serializer.validated_data)
