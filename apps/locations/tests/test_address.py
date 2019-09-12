import pytest

from rest_framework import status

from apps.locations.models import Address


@pytest.mark.django_db
class TestAddress:
    def test_create_address(self, client, user, token, address_dict):
        res = client.post('/api/addresses/', data=address_dict, **{'HTTP_AUTHORIZATION': 'Token ' + str(token)})
        assert res.status_code == status.HTTP_201_CREATED
        db_address = Address.objects.get(house=address_dict['house'])
        assert db_address.country == address_dict['country']
        assert db_address.city == address_dict['city']
        assert db_address.house == address_dict['house']

    def test_create_address__not_authenticated(self, client, address_dict):
        res = client.post('/api/addresses/', data=address_dict)
        assert res.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.parametrize('address_qty', [10, 20])
    def test_list(self, client, addresses, address_qty):
        res = client.get('/api/addresses/')
        assert res.status_code == status.HTTP_200_OK
        assert len(res.json()) == address_qty
