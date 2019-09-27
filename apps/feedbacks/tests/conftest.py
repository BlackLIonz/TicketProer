import pytest
from pytest_factoryboy import register
from rest_auth.app_settings import create_token, TokenSerializer
from rest_auth.models import TokenModel

from apps.events.factories import EventOrganizerWithPlaceFactory
from apps.feedbacks.factories import ReviewFactory
from apps.locations.factories import PlaceFactory, AddressFactory
from apps.users.factories import UserFactory, OrganizationFactory

register(UserFactory, 'user')
register(PlaceFactory, 'place')
register(OrganizationFactory, 'organization')
register(AddressFactory, 'address')
register(EventOrganizerWithPlaceFactory, 'event')


@pytest.fixture
def token(user):
    return create_token(TokenModel, user, TokenSerializer)


@pytest.fixture
def review_dict():
    return {
        'rating': 5,
        'text': 'Hello world'
    }


@pytest.fixture
def review_qty():
    return 1


@pytest.fixture
def reviews(review_qty, users, events, places, organizations):
    return ReviewFactory.create_batch(size=review_qty)


@pytest.fixture
def places():
    return PlaceFactory.create_batch(size=100)


@pytest.fixture
def events():
    return EventOrganizerWithPlaceFactory.create_batch(size=10)


@pytest.fixture
def organizations():
    return OrganizationFactory.create_batch(size=10)


@pytest.fixture
def users():
    return UserFactory.create_batch(size=10)
