import pytest
from rest_framework import status


@pytest.mark.django_db
class TestAddress:
    def test_create_address(self, client, user, token, place_dict):
        user.is_staff = True
        user.save()
        res = client.post('/api/places/', data=json.dumps(place_dict), content_type='application/json',
                          **{'HTTP_AUTHORIZATION': 'Token ' + str(token)})
        assert res.status_code == status.HTTP_201_CREATED
        res_place = res.json()
        assert res_place['id']
        db_place = Place.objects.get(id=res_place['id'])
        assert db_place.name == res_place.get('name')
        assert db_place.description == res_place.get('description')
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

    # @pytest.mark.parametrize('place_qty', [10, 20])
    # def test_update(self, client, places, place_dict, token, user, place_qty):
    #     new_place = {'name': 'Other House',
    #                  'address': {'country': 'Georgia',
    #                              'city': 'Tbilisi',
    #                              'house': '27',
    #                              'description': 'My other home'
    #                              }
    #                  }
    #     user.is_staff = True
    #     user.save()
    #     res = client.post('/api/places/', data=json.dumps(place_dict), content_type='application/json',
    #                       **{'HTTP_AUTHORIZATION': 'Token ' + str(token)})
    #     print(res.json())
    #     place = Place.objects.get(id=res.json().get('id'))
    #     res = client.put(f'/api/places/{str(place.id)}/', data=json.dumps(new_place),
    #                      content_type='application/json', **{'HTTP_AUTHORIZATION': 'Token ' + str(token)})
    #     assert res.status_code == status.HTTP_200_OK
    #     res_street = res.json()
    #     assert res_street.get('name') == new_place.get('name')
    #     assert res_street.get('status') == new_place.get('status')
    #     assert res_street.get('address').get('id') == new_place.get('address').get('id')
    #     assert res_street.get('description') == new_place.get('description')

    # def test_update__not_valid_data(self, client, address_dict, token, user):
    #     new_address = {'floor': '5', 'city': 'Tbilisi'}
    #     client.post('/api/addresses/', data=address_dict, **{'HTTP_AUTHORIZATION': 'Token ' + str(token)})
    #     address = Address.objects.get(created_by=user)
    #     res = client.put(f'/api/addresses/{str(address.id)}/', data=json.dumps(new_address),
    #                      content_type='application/json', **{'HTTP_AUTHORIZATION': 'Token ' + str(token)})
    #     assert res.status_code == status.HTTP_400_BAD_REQUEST

    # def test_update__not_owner(self, client, token, user, addresses):
    #     new_address = {'floor': '5', 'city': 'Tbilisi'}
    #     address = Address.objects.all()[0]
    #     res = client.put(f'/api/addresses/{str(address.id)}/', data=json.dumps(new_address),
    #                      content_type='application/json', **{'HTTP_AUTHORIZATION': 'Token ' + str(token)})
    #     assert res.status_code == status.HTTP_403_FORBIDDEN

    # def test_partial_update(self, client, addresses, address_dict, token, user, address_qty=10):
    #     new_address = {'country': 'Georgia'}
    #     client.post('/api/addresses/', data=address_dict, **{'HTTP_AUTHORIZATION': 'Token ' + str(token)})
    #     address = Address.objects.get(created_by=user)
    #     res = client.patch(f'/api/addresses/{str(address.id)}/', data=json.dumps(new_address),
    #                        content_type='application/json', **{'HTTP_AUTHORIZATION': 'Token ' + str(token)})
    #     assert res.status_code == status.HTTP_200_OK
    #     res_street = res.json()
    #     assert res_street['country'] == new_address['country']
