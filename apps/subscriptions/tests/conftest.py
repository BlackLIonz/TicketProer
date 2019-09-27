import pytest
from pytest_factoryboy import register
from rest_auth.models import TokenModel

from apps.events.factories import (
    EventUserWithoutPlaceFactory,
    EventUserWithPlaceFactory,
    EventOrganizerWithoutPlaceFactory,
    EventOrganizerWithPlaceFactory
)
from apps.locations.factories import AddressFactory, PlaceFactory
from apps.subscriptions.factories import SubscriptionFactory, ForTestsSubscriptionFactory
from apps.users.factories import UserFactory, OrganizationFactory

token_model = TokenModel
register(UserFactory, 'user')
register(UserFactory, 'request_user')
register(UserFactory, 'owner')
register(PlaceFactory, 'place')
register(AddressFactory, 'address')
register(OrganizationFactory, 'organization')
register(EventUserWithoutPlaceFactory, 'event')
register(EventUserWithoutPlaceFactory, 'event_created_by_user_without_place')
register(EventUserWithPlaceFactory, 'event_created_by_user_with_place')
register(EventOrganizerWithoutPlaceFactory, 'event_created_by_organization_without_place')
register(EventOrganizerWithPlaceFactory, 'event_created_by_organization_with_place')
register(SubscriptionFactory, 'subscription')


@pytest.fixture
def token(request_user):
    token, _ = token_model.objects.get_or_create(user=request_user)
    return token


@pytest.fixture
def subscription():
    return ForTestsSubscriptionFactory()


@pytest.fixture
def subscription_qty():
    return 1


@pytest.fixture
def subscriptions(subscription_qty):
    return ForTestsSubscriptionFactory.create_batch(size=subscription_qty)
