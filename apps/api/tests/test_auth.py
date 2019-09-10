import pytest

from rest_framework import status

from apps.users.models import User


@pytest.mark.django_db
class TestAuth:
    def test_registration(self, client):
        user_info = {
            'username': 'Bot',
            'email': 'bot@gmail.com',
            'password': 'botpass123',
            'first_name': 'Bot',
            'last_name': 'Botovich',
            'is_staff': True
        }
        res = client.post('/api/auth/registration/', data=user_info)
        assert res.status_code == status.HTTP_201_CREATED
        user = User.objects.get(email=user_info['email'])
        assert user.email == user_info['email']
        assert user.username == user_info['username']
        assert user.password != user_info['password']
        assert user.first_name == user_info['first_name']
        assert user.last_name == user_info['last_name']
        assert user.is_staff is False

    def test_login(self, client, user):
        login_info = {
            'email': user.email,
            'password': user.password,
        }
        print(user.__dict__)
        print(User.objects.all()[0].__dict__)
        res = client.post('/api/auth/login/', data=login_info)
        assert res.status_code == status.HTTP_200_OK
