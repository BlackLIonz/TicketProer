import pytest

from rest_framework import status

from apps.users.models import User
from rest_auth.models import TokenModel


@pytest.mark.django_db
class TestAuth:
    def test_registration(self, client, user_dict):
        res = client.post('/api/auth/registration/', data=user_dict)
        assert res.status_code == status.HTTP_201_CREATED
        user = User.objects.get(email=user_dict['email'])
        assert user.email == user_dict['email']
        assert user.username == user_dict['username']
        assert user.first_name == user_dict['first_name']
        assert user.last_name == user_dict['last_name']

    def test_is_staff_registration(self, client, user_dict):
        user_dict['is_staff'] = True
        res = client.post('/api/auth/registration/', data=user_dict)
        assert res.status_code == status.HTTP_201_CREATED
        user = User.objects.get(email=user_dict['email'])
        assert user.is_staff is False

    def test_login(self, client, user_dict):
        user = User.objects.create_user(**user_dict)
        res = client.post('/api/auth/login/', data={'email': user_dict['email'], 'password': user_dict['password']})
        assert res.status_code == status.HTTP_200_OK
        assert str(user.auth_token) == res.json()['key']

    def test_logout(self, client, user, token):
        res = client.post('/api/auth/logout/', **{'HTTP_AUTHORIZATION': 'Token ' + str(token)})
        assert res.status_code == status.HTTP_200_OK
        assert res.json()['detail'] == 'Successfully logged out.'
        assert not TokenModel.objects.filter(user=user).exists()
