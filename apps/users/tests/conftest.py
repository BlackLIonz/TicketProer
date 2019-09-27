import pytest
from pytest_factoryboy import register
from rest_auth.models import TokenModel

from apps.events.factories import EventUserWithPlaceFactory
from apps.locations.factories import PlaceFactory, AddressFactory
from apps.users.factories import UserFactory, OrganizationFactory

token_model = TokenModel
register(UserFactory, 'user')
register(UserFactory, 'request_user')
register(PlaceFactory, 'place')
register(AddressFactory, 'address')
register(OrganizationFactory, 'organization')
register(EventUserWithPlaceFactory, 'event')


@pytest.fixture
def token(request_user):
    token, _ = token_model.objects.get_or_create(user=request_user)
    return token


@pytest.fixture
def event_qty():
    return 1


@pytest.fixture
def events(event_qty):
    return EventUserWithPlaceFactory.create_batch(size=event_qty)
