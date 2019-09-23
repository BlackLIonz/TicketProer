import pytest
from rest_auth.app_settings import create_token, TokenSerializer
from rest_auth.models import TokenModel
from pytest_factoryboy import register

from apps.users.factories import UserFactory


register(UserFactory, 'user')


@pytest.fixture
def user_dict():
    return {
        'username': 'Bot',
        'email': 'bot@gmail.com',
        'password': 'botpass123',
        'first_name': 'Bot',
        'last_name': 'Botovich'
    }


@pytest.fixture
def token(user):
    return create_token(TokenModel, user, TokenSerializer)
