import uuid

from django_filters import rest_framework as filters
from rest_framework import viewsets, exceptions, status, filters as rest_filters
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from apps.events.models import Event
from apps.subscriptions.models import Subscription
from apps.subscriptions.serializers import SubscriptionSerializer
from tools.action_based_permission import ActionBasedPermission
from tools.custom_permissions import IsSubscriberOrAdmin


class SubscriptionFilter(filters.FilterSet):
    class Meta:
        model = Subscription
        fields = {
            'event': ['exact'],
            'user': ['exact'],
            'status': ['exact'],
            'event__date': ['lte', 'gte'],
            'event__organizer_type': ['exact'],
            'event__organizer_id': ['exact']
        }


class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    filter_backends = [filters.DjangoFilterBackend, rest_filters.OrderingFilter]
    filterset_class = SubscriptionFilter
    ordering_fields = ('event__date',)
    ordering = ('event__date',)
    permission_classes = (ActionBasedPermission,)
    action_permissions = {
        IsAdminUser: ['list', 'update', 'partial_update'],
        IsAuthenticated: ['create', 'destroy', 'approve'],
        IsSubscriberOrAdmin: ['retrieve'],
    }

    def create(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        subscribed_event_id = self.get_event_id(data)
        if not subscribed_event_id:
            raise exceptions.ParseError('Please, transmit event as dict or str.')
        subscribed_event = self.get_obj_by_id(subscribed_event_id, Event)
        if not subscribed_event.is_available_for_subscription:
            raise exceptions.PermissionDenied('Too late to subscribe.')
        response = self.create_subscription(user, subscribed_event)
        return response

    def retrieve(self, request, *args, **kwargs):
        subscription = self.get_object()
        if subscription.status == Subscription.STATUS_CANCELLED:
            raise exceptions.NotFound('No subscription found.')
        serializer_data = SubscriptionSerializer(subscription).data
        return Response(serializer_data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        subscription = self.get_object()
        if not request.user == subscription.user:
            raise exceptions.PermissionDenied('You could delete only your own subscriptions.')
        if subscription.status == Subscription.STATUS_CANCELLED:
            raise exceptions.NotFound('No subscription found.')
        subscription.set_status(Subscription.STATUS_CANCELLED)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        approved_subscription = self.get_obj_by_id(pk, Subscription)
        if not request.user == approved_subscription.user:
            raise exceptions.PermissionDenied('You could approve only your own subscriptions.')
        if not approved_subscription.event.is_available_for_subscription:
            raise exceptions.PermissionDenied('Too late to subscribe.')
        response = self.approve_subscription(approved_subscription)
        return response

    def get_event_id(self, data):
        event = data.pop('event', None)
        if event is None:
            raise exceptions.ParseError('You must transmit event id.')
        if not isinstance(event, (str, dict)):
            raise exceptions.ParseError('Please, transmit event as dict or str.')
        return event if isinstance(event, str) else event.get('id')

    def get_obj_by_id(self, obj_id, cls):
        try:
            return cls.objects.get(id=uuid.UUID(str(obj_id)))
        except ValueError:
            raise exceptions.ParseError(f'{cls.__name__}\'s ID is not valid.')
        except cls.DoesNotExist:
            raise exceptions.NotFound('No such ID in database.')

    def create_subscription(self, user, event):
        duplicate = Subscription.objects.all().filter(user=user, event=event).first()
        if not duplicate:
            subscription = Subscription.objects.create(user=user, event=event)
            subscription_data = SubscriptionSerializer(subscription).data
            return Response(subscription_data, status=status.HTTP_201_CREATED)
        if duplicate.status in (
                Subscription.STATUS_ACTIVE,
                Subscription.STATUS_UNTRACKED,
                Subscription.STATUS_REJECTED,
                ):
            return Response(status=status.HTTP_409_CONFLICT)
        if duplicate.status == Subscription.STATUS_CANCELLED:
            duplicate.set_status(Subscription.STATUS_UNTRACKED)
            duplicate_data = SubscriptionSerializer(duplicate).data
            return Response(duplicate_data, status=status.HTTP_201_CREATED)

    def approve_subscription(self, subscription):
        if subscription.status == Subscription.STATUS_UNTRACKED:
            subscription.set_status(Subscription.STATUS_ACTIVE)
            subscription_data = SubscriptionSerializer(subscription).data
            return Response(subscription_data, status=status.HTTP_200_OK)
        if subscription.status == Subscription.STATUS_ACTIVE:
            return Response(status=status.HTTP_409_CONFLICT)
        if subscription.status == Subscription.STATUS_REJECTED:
            return Response(status=status.HTTP_403_FORBIDDEN)
        if subscription.status == Subscription.STATUS_CANCELLED:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class SubscriptionMeViewSet(viewsets.ReadOnlyModelViewSet):

    model = Subscription
    serializer_class = SubscriptionSerializer
    filter_backends = [filters.DjangoFilterBackend, rest_filters.OrderingFilter]
    filterset_class = SubscriptionFilter

    ordering_fields = ('event__date',)
    ordering = ('event__date',)

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.all_active_subscriptions
