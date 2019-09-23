import pytest
import faker
from rest_framework import status


@pytest.mark.django_db
class TestPlaces:
    def test_detail(self, client, place):
        res = client.get(f'/api/places/{place.id}/')
        assert res.status_code == status.HTTP_200_OK
        place_dict = res.json()
        assert place_dict.get('id') == str(place.id)
        assert place_dict.get('name') == place.name

        address = place_dict.get('address')
        assert address
        assert address.get('id') == str(place.address.id)
        assert address.get('country') == place.address.country
        assert address.get('city') == place.address.city
        assert address.get('street') == place.address.street
        assert address.get('house') == place.address.house
        assert address.get('floor') == place.address.floor
        assert address.get('apartments') == place.address.apartments
        assert address.get('description') == place.address.description

        assert place_dict.get('description') == place.description
        assert place_dict.get('status') == place.status

    @pytest.mark.parametrize('place_qty', [0, 1, 10, 50])
    def test_list(self, client, places, place_qty):
        res = client.get('/api/places/')
        assert res.status_code == status.HTTP_200_OK
        assert isinstance(res.json(), list)
        assert len(res.json()) == place_qty

    def test_detail_error(self, client):
        res = client.get(f'api/places/{faker.Faker().random_number()}/')
        assert res.status_code == status.HTTP_404_NOT_FOUND
