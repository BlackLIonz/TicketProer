import datetime
import json

import pytest
import random

import pytz
from rest_framework import status

from apps.locations.models import Address


@pytest.mark.django_db
class TestAddress:
    def test_create_address(self, client, user, token, address_dict):
        res = client.post('/api/addresses/', data=address_dict, **{'HTTP_AUTHORIZATION': 'Token ' + str(token)})
        assert res.status_code == status.HTTP_201_CREATED
        db_address = Address.objects.get(id=res.json()['id'])
        assert db_address.country == address_dict['country']
        assert db_address.city == address_dict['city']
        assert db_address.house == address_dict['house']

    def test_create_address_not_authenticated(self, client, address_dict):
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
        db_address = Address.objects.get(id=addresses[i].id)
        assert res.status_code == status.HTTP_200_OK
        address = res.json()
        assert address['id'] == str(db_address.id)
        assert address['country'] == db_address.country
        assert address['city'] == db_address.city
        assert address['street'] == str(db_address.street)
        assert address['house'] == str(db_address.house)
        assert address['floor'] == db_address.floor
        assert address['apartments'] == str(db_address.apartments)
        assert address['description'] == db_address.description
        assert datetime.datetime.strptime(
            address['created'], '%Y-%m-%dT%H:%M:%S.%fZ').replace(tzinfo=pytz.UTC) == db_address.created
        assert address['created_by'] == str(db_address.created_by.id)

    def test_retrieve_not_found(self, client, addresses, address_qty=10):
        res = client.get(f'/api/addresses/dmbkdlf/')
        assert res.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.parametrize('address_qty', [10, 20])
    def test_update(self, client, addresses, address_dict, token, user, address_qty):
        new_address = {'country': 'Georgia', 'city': 'Tbilisi'}
        res = client.post('/api/addresses/', data=address_dict, **{'HTTP_AUTHORIZATION': 'Token ' + str(token)})
        address = Address.objects.get(id=res.json()['id'])
        res = client.put(f'/api/addresses/{str(address.id)}/', data=json.dumps(new_address),
                         content_type='application/json', **{'HTTP_AUTHORIZATION': 'Token ' + str(token)})
        assert res.status_code == status.HTTP_200_OK
        res_street = res.json()
        assert res_street['country'] == new_address['country']
        assert res_street['city'] == new_address['city']

    def test_update_not_valid_data(self, client, address_dict, token, user):
        new_address = {'floor': '5', 'city': 'Tbilisi'}
        client.post('/api/addresses/', data=address_dict, **{'HTTP_AUTHORIZATION': 'Token ' + str(token)})
        address = Address.objects.get(created_by=user)
        res = client.put(f'/api/addresses/{str(address.id)}/', data=json.dumps(new_address),
                         content_type='application/json', **{'HTTP_AUTHORIZATION': 'Token ' + str(token)})
        assert res.status_code == status.HTTP_400_BAD_REQUEST

    def test_update_not_owner(self, client, token, user, addresses):
        new_address = {'country': 'Georgia', 'city': 'Tbilisi'}
        address = Address.objects.all().first()
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
