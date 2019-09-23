import pytest
from rest_framework import status
from rest_auth.models import TokenModel

from apps.users.models import User


@pytest.mark.django_db
class TestAuth:
    def test_registration(self, client, user_dict):
        res = client.post('/api/auth/registration/', data=user_dict)
        assert res.status_code == status.HTTP_201_CREATED
        user = User.objects.get(email=user_dict.get('email'))
        assert user.email == user_dict.get('email')
        assert user.username == user_dict.get('username')
        assert user.first_name == user_dict.get('first_name')
        assert user.last_name == user_dict.get('last_name')

    def test_registration_with_is_staff(self, client, user_dict):
        user_dict['is_staff'] = True
        res = client.post('/api/auth/registration/', data=user_dict)
        assert res.status_code == status.HTTP_201_CREATED
        user = User.objects.get(email=user_dict.get('email'))
        assert user.is_staff is False

    def test_login(self, client, user_dict):
        user = User.objects.create_user(**user_dict)
        res = client.post('/api/auth/login/', data={'email': user_dict.get('email'), 'password': user_dict.get('password')})
        assert res.status_code == status.HTTP_200_OK
        assert str(user.auth_token) == res.json().get('key')

    def test_logout(self, client, user, token):
        res = client.post('/api/auth/logout/', **{'HTTP_AUTHORIZATION': 'Token ' + str(token)})
        assert res.status_code == status.HTTP_200_OK
        assert res.json().get('detail') == 'Successfully logged out.'
        assert not TokenModel.objects.filter(user=user).exists()
