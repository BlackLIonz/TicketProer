import pytest

from pytest_factoryboy import register
from rest_auth.models import TokenModel
from rest_auth.app_settings import create_token, TokenSerializer

from apps.locations.models import Place
from apps.users.factories import UserFactory
from apps.locations.factories import AddressFactory, PlaceFactory


register(UserFactory, 'user')
register(PlaceFactory, 'place')
register(AddressFactory, 'address')
  
  
@pytest.fixture
def token(user):
    return create_token(TokenModel, user, TokenSerializer)


@pytest.fixture
def place():
    return PlaceFactory()
  
  
@pytest.fixture
def address_qty():
  return 1


@pytest.fixture
def token(user):
    return create_token(TokenModel, user, TokenSerializer)


@pytest.fixture
def place_qty():
    return 1

  
@pytest.fixture
def address_dict():
    return {
        'country': 'Belarus',
        'city': 'Minsk',
        'house': '17A'
    }

  
@pytest.fixture
def address_qty():
    return 1


@pytest.fixture
def place_dict():
    return {
        'name': 'Home',
        'address': {
            'country': 'Belarus',
            'city': 'Minsk',
            'house': '17A',
            'description': 'My home'
        },
        'status': Place.STATUS_WORKING,
        'description': 'house',
    }


@pytest.fixture
def place_dict_address_id():
    address = AddressFactory()
    return {
        'name': 'Home',
        'address': str(address.id),
        'status': Place.STATUS_WORKING,
        'description': 'house',
    }


@pytest.fixture
def places(place_qty):
    return PlaceFactory.create_batch(size=place_qty)

@pytest.fixture
def addresses(address_qty):
    return AddressFactory.create_batch(size=address_qty)
