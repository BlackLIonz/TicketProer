import json

import pytest
import random

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

    @pytest.mark.parametrize('address_qty', [10, 20])
    def test_retrieve(self, client, addresses, address_qty):
        i = random.randint(0, len(addresses) - 1)
        res = client.get(f'/api/addresses/{str(addresses[i].id)}/')
        assert res.status_code == status.HTTP_200_OK
        address = res.json()
        assert address['id'] == str(addresses[i].id)
        assert address['created_by'] == str(addresses[i].created_by.id)
        assert address['country'] == addresses[i].country
        assert address['city'] == addresses[i].city

    def test_retrive__not_found(self, client, addresses, address_qty=10):
        res = client.get(f'/api/addresses/dmbkdlf/')
        assert res.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.parametrize('address_qty', [10, 20])
    def test_update(self, client, addresses, address_dict, token, user, address_qty):
        new_address = {'country': 'Georgia', 'city': 'Tbilisi'}
        client.post('/api/addresses/', data=address_dict, **{'HTTP_AUTHORIZATION': 'Token ' + str(token)})
        address = Address.objects.get(created_by=user)
        res = client.put(f'/api/addresses/{str(address.id)}/', data=json.dumps(new_address),
                         content_type='application/json', **{'HTTP_AUTHORIZATION': 'Token ' + str(token)})
        assert res.status_code == status.HTTP_200_OK
        res_street = res.json()
        assert res_street['country'] == new_address['country']
        assert res_street['city'] == new_address['city']

    def test_update__not_valid_data(self, client, address_dict, token, user):
        new_address = {'floor': '5', 'city': 'Tbilisi'}
        client.post('/api/addresses/', data=address_dict, **{'HTTP_AUTHORIZATION': 'Token ' + str(token)})
        address = Address.objects.get(created_by=user)
        res = client.put(f'/api/addresses/{str(address.id)}/', data=json.dumps(new_address),
                         content_type='application/json', **{'HTTP_AUTHORIZATION': 'Token ' + str(token)})
        assert res.status_code == status.HTTP_400_BAD_REQUEST

    def test_update__not_owner(self, client, token, user, addresses):
        new_address = {'floor': '5', 'city': 'Tbilisi'}
        address = Address.objects.all()[0]
        res = client.put(f'/api/addresses/{str(address.id)}/', data=json.dumps(new_address),
                         content_type='application/json', **{'HTTP_AUTHORIZATION': 'Token ' + str(token)})
        assert res.status_code == status.HTTP_403_FORBIDDEN

    def test_partial_update(self, client, addresses, address_dict, token, user, address_qty=10):
        new_address = {'country': 'Georgia'}
        client.post('/api/addresses/', data=address_dict, **{'HTTP_AUTHORIZATION': 'Token ' + str(token)})
        address = Address.objects.get(created_by=user)
        res = client.patch(f'/api/addresses/{str(address.id)}/', data=json.dumps(new_address),
                           content_type='application/json', **{'HTTP_AUTHORIZATION': 'Token ' + str(token)})
        assert res.status_code == status.HTTP_200_OK
        res_street = res.json()
        assert res_street['country'] == new_address['country']
