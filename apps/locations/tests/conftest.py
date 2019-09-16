import pytest
from pytest_factoryboy import register
from rest_auth.models import TokenModel
from rest_auth.app_settings import create_token, TokenSerializer

from apps.locations.models import Place
from apps.users.factories import UserFactory
from apps.locations.factories import PlaceFactory


register(UserFactory, 'user')
register(PlaceFactory, 'place')
register(PlaceFactory, 'address')


@pytest.fixture
def token(user):
    return create_token(TokenModel, user, TokenSerializer)


@pytest.fixture
def place_qty():
    return 1


@pytest.fixture
def place_dict():
    return {
        "name": "Home",
        "address": {
            "country": "Belarus",
            "city": "Minsk",
            "house": "17A",
            "description": "My home"
        },
        "status": Place.STATUS_WORKING,
        "description": "Shota's house"
    }


@pytest.fixture
def places(place_qty):
    return PlaceFactory.create_batch(size=place_qty)
