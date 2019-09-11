import pytest

from apps.users.tests.factories.users import UserFactory
from pytest_factoryboy import register
from rest_auth.models import TokenModel
# from apps.users.tests.test_user import token

token_model = TokenModel
register(UserFactory, 'staff')
register(UserFactory, 'user')


@pytest.fixture
def token(staff):
    token, _ = token_model.objects.get_or_create(user=staff)
    return token


@pytest.mark.django_db
class TestStaff:
    def test_user_details_for_staff(self, client, staff, user, token):
        staff.is_staff = True
        staff.save()
        response = client.get(f'/api/user/{user.id}/', **{'HTTP_AUTHORIZATION': 'Token ' + str(token)})
        response_dict = response.json()
        assert response.status_code == 200
        assert response_dict.get('username')
        assert response_dict.get('email')
        assert response_dict.get('id')
        assert response_dict.get('created')
        assert response_dict.get('updated')
        assert response_dict.get('first_name')
        assert response_dict.get('last_name')
        assert response_dict.get('date_of_birth')
        assert response_dict.get('password') is None
        assert response_dict.get('is_staff') is False
        assert response_dict.get('is_active') is True
        assert response_dict.get('profile_image') is None