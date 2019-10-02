from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, exceptions
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from drf_yasg.openapi import Response as SwgResponse

from apps.base.views import ReviewsMixin
from apps.locations.models import Place, Address
from apps.locations.serializers import PlaceSerializer, AddressSerializer
from tools.action_based_permission import ActionBasedPermission
from tools.custom_permissions import IsOwnerOrAdmin


@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_summary='List method that lists all places.',
    operation_description='Lists all created Places. This endpoint is reachable by anyone.',
    responses={
        '200': SwgResponse('Ok. List returned.', PlaceSerializer()),
    }
    )
)
@method_decorator(name='retrieve', decorator=swagger_auto_schema(
    operation_summary='Retrieve method that gives detailed information about place.',
    operation_description='Gives detailed information about Place. This endpoint is reachable by anyone.',
    responses={
        '200': SwgResponse('Ok. Place returned.', PlaceSerializer()),
        '404': 'Not found. Bad Place id.',
    }
    )
)
class PlaceViewSet(viewsets.ModelViewSet, ReviewsMixin):
    """
    A viewset that provides `create()`, `retrieve()`, `update()`,
    `partial_update()`, `destroy()` and `list()` actions.
    """
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    permission_classes = (ActionBasedPermission,)
    action_permissions = {
        AllowAny: ['retrieve', 'list', 'reviews'],
        IsAdminUser: ['destroy', 'create', 'update', 'partial_update'],
    }

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        self._update_address(instance)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        data = request.data
        address = self._create_address()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        place = self.perform_create(serializer, address=address)
        place_data = serializer_class(place).data
        headers = self.get_success_headers(place_data)
        return Response(place_data, status=status.HTTP_201_CREATED, headers=headers)

    def _create_address(self):
        if 'address' in self.request.data:
            address_data = self.request.data.pop('address')
        else:
            raise exceptions.ParseError('Address field is empty')
        if isinstance(address_data, str):
            return Address.objects.get(pk=address_data)
        elif isinstance(address_data, dict):
            address_ser = AddressSerializer(data=address_data)
            if address_ser.is_valid():
                return Address.objects.create(**address_ser.validated_data)
        raise exceptions.ParseError('Address invalid')

    def _update_address(self, instance):
        data = self.request.data
        if 'address' in data:
            address_id = data.pop('address')
            address_instance = get_object_or_404(Address, id=address_id)
            instance.address = address_instance

    def perform_create(self, serializer, **kwargs):
        return Place.objects.create(**kwargs, **serializer.validated_data)


@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_summary='List method that lists all addresses.',
    operation_description='Lists all created Addresses. This endpoint is reachable by anyone.',
    responses={
        '200': SwgResponse('Ok. List returned.', AddressSerializer()),
    }
    )
)
@method_decorator(name='retrieve', decorator=swagger_auto_schema(
    operation_summary='Retrieve method that gives detailed information about address.',
    operation_description='Gives detailed information about Address. This endpoint is reachable by anyone.',
    responses={
        '200': SwgResponse('Ok. Address returned.', AddressSerializer()),
        '404': 'Not found. Bad Address id.',
    }
    )
)
class AddressViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides `create()`, `retrieve()`, `update()`,
    `partial_update()`, `destroy()` and `list()` actions.
    """

    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = (ActionBasedPermission,)
    action_permissions = {
        IsOwnerOrAdmin: ['update', 'partial_update'],
        AllowAny: ['retrieve', 'list'],
        IsAuthenticated: ['create'],
        IsAdminUser: ['destroy'],
    }

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
