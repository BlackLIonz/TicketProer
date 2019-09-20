import json
import random

import pytest
from rest_framework import status

from apps.locations.models import Place


@pytest.mark.django_db
class TestPlace:
    def test_create_place_with_address_dict(self, client, user, token, place_dict):
        user.is_staff = True
        user.save()
        res = client.post('/api/places/', data=json.dumps(place_dict), content_type='application/json',
                          **{'HTTP_AUTHORIZATION': 'Token ' + str(token)})
        assert res.status_code == status.HTTP_201_CREATED
        res_place = res.json()
        assert res_place['id']
        db_place = Place.objects.get(id=res_place['id'])
        assert db_place.name == res_place.get('name')
        assert db_place.status == res_place.get('status')
        assert str(db_place.address.id) == res_place.get('address').get('id')

    @pytest.mark.parametrize('place_qty', [10, 50])
    def test_create_place_with_address_id(self, client, user, token, place_qty, place_dict_address_id):
        user.is_staff = True
        user.save()
        res = client.post('/api/places/', data=json.dumps(place_dict_address_id), content_type='application/json',
                          **{'HTTP_AUTHORIZATION': 'Token ' + str(token)})
        assert res.status_code == status.HTTP_201_CREATED
        res_place = res.json()
        assert res_place['id']
        db_place = Place.objects.get(id=res_place['id'])
        assert db_place.name == res_place.get('name')
        assert db_place.status == res_place.get('status')
        assert str(db_place.address.id) == res_place.get('address').get('id')

    def test_create_place_not_authenticated(self, client, place_dict):
        res = client.post('/api/places/', data=json.dumps(place_dict), content_type='application/json')
        assert res.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.parametrize('place_qty', [10, 20])
    def test_list_place(self, client, places, place_qty):
        res = client.get('/api/places/')
        assert res.status_code == status.HTTP_200_OK
        assert len(res.json()) == place_qty

    @pytest.mark.parametrize('places_qty', [10, 20])
    def test_retrieve_place(self, client, places, places_qty):
        i = random.randint(0, len(places) - 1)
        res = client.get(f'/api/places/{str(places[i].id)}/')
        assert res.status_code == status.HTTP_200_OK
        place = res.json()
        assert places[i].name == place.get('name')
        assert places[i].description == place.get('description')
        assert places[i].status == place.get('status')
        assert str(places[i].address.id) == place.get('address').get('id')

    def test_retrieve_place_not_found(self, client, places, places_qty=10):
        res = client.get(f'/api/places/dmbkdlf/')
        assert res.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.parametrize('place_qty', [10, 20])
    def test_update(self, client, places, address, place_dict, token, user, place_qty):
        new_place = {
            'name': 'Other House',
            'address': str(address.id),
        }
        user.is_staff = True
        user.save()
        res = client.post('/api/places/', data=json.dumps(place_dict), content_type='application/json',
                          **{'HTTP_AUTHORIZATION': 'Token ' + str(token)})
        place = Place.objects.get(id=res.json().get('id'))
        res = client.put(f'/api/places/{str(place.id)}/', data=json.dumps(new_place),
                         content_type='application/json', **{'HTTP_AUTHORIZATION': 'Token ' + str(token)})
        new_place = Place.objects.get(pk=res.json().get('id'))
        assert res.status_code == status.HTTP_200_OK
        res_street = res.json()
        assert res_street.get('name') == new_place.name
        assert res_street.get('status') == new_place.status
        assert res_street.get('address').get('id') == str(new_place.address.id)
        assert res_street.get('description') == new_place.description

    def test_update_address_invalid(self, client, places, address, place_dict, token, user, place_qty):
        new_place = {
            'name': 'Other House',
            'address': str(address.id),
        }
        user.is_staff = True
        user.save()
        res = client.post('/api/places/', data=json.dumps(place_dict), content_type='application/json',
                          **{'HTTP_AUTHORIZATION': 'Token ' + str(token)})
        res = client.put(f'/api/places/f867bb77-8d4d-4c88-9e04-e1651ea05vgt2/', data=json.dumps(new_place),
                         content_type='application/json', **{'HTTP_AUTHORIZATION': 'Token ' + str(token)})
        assert res.status_code == status.HTTP_404_NOT_FOUND
