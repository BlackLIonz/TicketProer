import uuid

from django.contrib.contenttypes.models import ContentType
from django.utils.decorators import method_decorator
from django_filters import rest_framework as filters
from rest_framework import viewsets, mixins, status, exceptions, filters as rest_filters
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg.openapi import Response as SwgResponse

from apps.base.filters import AddressFilter, PlaceFilter, DateFilter
from apps.base.views import ReviewsMixin
from apps.events.models import Event
from apps.events.serializers import EventSerializer
from apps.locations.models import Place, Address
from apps.locations.serializers import AddressSerializer
from apps.users.models import User
from tools.action_based_permission import ActionBasedPermission


class EventFilter(PlaceFilter, AddressFilter, DateFilter):
    organizer = filters.UUIDFilter(field_name='organizer_id')
    is_top = filters.BooleanFilter(field_name='is_top')
    is_hot = filters.BooleanFilter(field_name='is_hot')

    class Meta:
        model = Event
        fields = ['place', 'address', 'organizer', 'date__lte', 'date__gte', 'is_top', 'is_hot']


@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_summary='This endpoint returns list of all created Events',
    operation_description=
    """
        This endpoint allows any user to access it
        This list supports: 
        1) Ordering on field created date.
        2) Filtering on fields Place, Address, Organizer, Date, Is top, Is hot
    """,
    responses={
        '200': SwgResponse('`Ok` List returned', EventSerializer()),
    }
))
@method_decorator(name='create', decorator=swagger_auto_schema(
    operation_summary='That endpoint creates new Event by any authenticated user',
    operation_description=
    """
        This endpoint allows any authenticated user to access it
        Options how to create Event:
        1) Supply Event's required data and Address' required data to create new Event with the new Address
        2) Supply Event's required data and Address' id to create new Event with already existed Address
        3) Supply Event's required data and Place's id to create new Event with already existed Place
    """,
    responses={
        '201': SwgResponse('`Created` New Event returned', EventSerializer()),
        '400': 'Bad request',
        '404': 'Not found',
    }
))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(
    operation_summary='That endpoint represents detailed information of the Event',
    operation_description=
    """
        This endpoint allows any user to access it
        Collects detailed information about any existed event
    """,
    responses={
        '200': SwgResponse('Ok. Detailed information returned', EventSerializer()),
        '404': 'Not Found',
    }
))
class EventViewSet(mixins.CreateModelMixin,
                   viewsets.ReadOnlyModelViewSet,
                   ReviewsMixin):
    """
    A ViewSet which provides `retrieve()`,
    `list()` and `create()` actions
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = (ActionBasedPermission,)
    action_permissions = {
        AllowAny: ['retrieve', 'list', 'reviews'],
        IsAuthenticated: ['create'],
    }
    filter_backends = [filters.DjangoFilterBackend, rest_filters.OrderingFilter]
    filterset_class = EventFilter

    ordering_fields = ('created',)
    ordering = ('created',)

    def create(self, request, *args, **kwargs):
        user = request.user
        data_dict = request.data
        place = None
        address = None
        receive_place_mapping = {
            dict: lambda obj: self.get_created_object(obj.get('id'), Place),
            str: lambda obj: self.get_created_object(obj, Place),
        }

        if 'place' in data_dict:
            place = data_dict.pop('place')
        if 'address' in data_dict:
            address = data_dict.pop('address')

        if isinstance(place, (dict, str)):
            place = receive_place_mapping.get(type(place))(place)
            address = self.get_created_object(place.address_id, Address)
        elif not isinstance(address, (dict, str)):
            raise exceptions.ParseError('Please, transmit address or place as dict or str')
        else:
            created_address_id = address if isinstance(address, str) else address.get('id')
            if created_address_id:
                address = self.get_created_object(created_address_id, Address)
            else:
                address_serializer = AddressSerializer(data=address)
                if not address_serializer.is_valid():
                    raise exceptions.ParseError('Address data is invalid')
                address = Address.objects.create(**address_serializer.validated_data)

        organizer, data_dict = self.choose_event_organizer(user=user, **data_dict)
        data_dict = self.set_defaults(**data_dict)
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=data_dict)
        serializer.is_valid(raise_exception=True)
        event = self.perform_create(serializer, address=address, place=place, organizer=organizer)
        event_data = serializer_class(event).data
        headers = self.get_success_headers(event_data)
        return Response(event_data, status=status.HTTP_201_CREATED, headers=headers)

    def get_created_object(self, obj_id, cls):
        """Validates ID"""
        try:
            return cls.objects.get(id=uuid.UUID(str(obj_id)))
        except ValueError:
            raise exceptions.ParseError(f'{cls.__name__}\'s ID is not valid')
        except cls.DoesNotExist:
            raise exceptions.NotFound('No such ID in database')

    def choose_event_organizer(self, user, **data_dict):
        """Checks if a user is a member of any organization"""
        try:
            organizer = user.membership.organization
        except User.membership.RelatedObjectDoesNotExist:
            organizer = user
        organizer_id, organizer_type = (
            organizer.id,
            ContentType.objects.get_for_model(organizer.__class__)
        )
        data_dict.update(dict(organizer_id=organizer_id, organizer_type=organizer_type))
        return organizer, data_dict

    def set_defaults(self, **data_dict):
        """Set defaults to important fields"""
        defaults = {
            'is_top': False,
            'is_hot': False,
            'is_approved': False,
            'status': Event.SOON,
        }
        data_dict.update(defaults)
        return data_dict

    def perform_create(self, serializer, **kwargs):
        return Event.objects.create(**kwargs, **serializer.validated_data)
