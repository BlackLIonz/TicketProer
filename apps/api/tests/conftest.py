import pytest

from pytest_factoryboy import register

from apps.users.factories import UserFactory

register(UserFactory, 'user')
