import datetime
import json

import faker
import pytest
import pytz
from rest_framework import status

from apps.events.models import Event
from apps.locations.models import Address, Place


@pytest.mark.django_db
class TestEvents:
    """
    poster in Event is always None,
    because we do not generate it
    """

    def test_detail_event_by_user_without_place(self, client, event_created_by_user_without_place):
        res = client.get(f'/api/events/{event_created_by_user_without_place.id}/')
        assert res.status_code == status.HTTP_200_OK
        event_dict = res.json()
        assert event_dict.get('name') == event_created_by_user_without_place.name
        assert event_dict.get('description') == event_created_by_user_without_place.description
        assert event_dict.get('poster') == event_created_by_user_without_place.poster
        assert event_dict.get('organizer_id') == str(event_created_by_user_without_place.organizer_id)
        assert event_dict.get('organizer_type') == str(event_created_by_user_without_place.organizer_type).title()

        organizer = event_dict.get('organizer')
        assert organizer
        assert organizer.get('id') == str(event_created_by_user_without_place.organizer.id)
        assert organizer.get('username') == event_created_by_user_without_place.organizer.username
        assert organizer.get('email') == event_created_by_user_without_place.organizer.email

        address = event_dict.get('address')
        assert address
        assert address.get('id') == str(event_created_by_user_without_place.address.id)
        assert address.get('country') == event_created_by_user_without_place.address.country
        assert address.get('city') == event_created_by_user_without_place.address.city
        assert address.get('street') == event_created_by_user_without_place.address.street
        assert address.get('house') == event_created_by_user_without_place.address.house
        assert address.get('floor') == event_created_by_user_without_place.address.floor
        assert address.get('apartments') == event_created_by_user_without_place.address.apartments
        assert address.get('description') == event_created_by_user_without_place.address.description
        assert datetime.datetime.strptime(
            address.get('created'), '%Y-%m-%dT%H:%M:%S.%fZ'
        ).replace(tzinfo=pytz.UTC) == event_created_by_user_without_place.address.created
        assert datetime.datetime.strptime(
            address.get('updated'), '%Y-%m-%dT%H:%M:%S.%fZ'
        ).replace(tzinfo=pytz.UTC) == event_created_by_user_without_place.address.updated

        assert datetime.datetime.strptime(
            event_dict.get('date'), '%Y-%m-%dT%H:%M:%SZ'
        ).replace(tzinfo=pytz.UTC) == event_created_by_user_without_place.date
        assert event_dict.get('duration') == event_created_by_user_without_place.duration
        assert event_dict.get('age_rate') == event_created_by_user_without_place.age_rate
        assert event_dict.get('is_approved') == event_created_by_user_without_place.is_approved
        assert event_dict.get('is_hot') == event_created_by_user_without_place.is_hot
        assert event_dict.get('is_top') == event_created_by_user_without_place.is_top
        assert event_dict.get('max_members') == event_created_by_user_without_place.max_members
        assert event_dict.get('status') == event_created_by_user_without_place.status
        assert datetime.datetime.strptime(
            event_dict.get('created'), '%Y-%m-%dT%H:%M:%S.%fZ'
        ).replace(tzinfo=pytz.UTC) == event_created_by_user_without_place.created
        assert datetime.datetime.strptime(
            event_dict.get('updated'), '%Y-%m-%dT%H:%M:%S.%fZ'
        ).replace(tzinfo=pytz.UTC) == event_created_by_user_without_place.updated

    def test_detail_event_by_user_with_place(self, client, event_created_by_user_with_place):
        res = client.get(f'/api/events/{event_created_by_user_with_place.id}/')
        assert res.status_code == status.HTTP_200_OK
        event_dict = res.json()
        assert event_dict.get('name') == event_created_by_user_with_place.name
        assert event_dict.get('description') == event_created_by_user_with_place.description
        assert event_dict.get('poster') == event_created_by_user_with_place.poster
        assert event_dict.get('organizer_id') == str(event_created_by_user_with_place.organizer_id)
        assert event_dict.get('organizer_type') == str(event_created_by_user_with_place.organizer_type).title()

        organizer = event_dict.get('organizer')
        assert organizer
        assert organizer.get('id') == str(event_created_by_user_with_place.organizer.id)
        assert organizer.get('username') == event_created_by_user_with_place.organizer.username
        assert organizer.get('email') == event_created_by_user_with_place.organizer.email

        place = event_dict.get('place')
        assert place
        assert place.get('id') == str(event_created_by_user_with_place.place.id)
        assert place.get('name') == event_created_by_user_with_place.place.name
        assert place.get('description') == event_created_by_user_with_place.place.description
        assert datetime.datetime.strptime(
            place.get('created'), '%Y-%m-%dT%H:%M:%S.%fZ'
        ).replace(tzinfo=pytz.UTC) == event_created_by_user_with_place.place.created
        assert place.get('status') == event_created_by_user_with_place.place.status

        address = event_dict.get('address')
        assert address
        assert address.get('id') == str(event_created_by_user_with_place.address.id)
        assert address.get('country') == event_created_by_user_with_place.address.country
        assert address.get('city') == event_created_by_user_with_place.address.city
        assert address.get('street') == event_created_by_user_with_place.address.street
        assert address.get('house') == event_created_by_user_with_place.address.house
        assert address.get('floor') == event_created_by_user_with_place.address.floor
        assert address.get('apartments') == event_created_by_user_with_place.address.apartments
        assert address.get('description') == event_created_by_user_with_place.address.description
        assert datetime.datetime.strptime(
            address.get('created'), '%Y-%m-%dT%H:%M:%S.%fZ'
        ).replace(tzinfo=pytz.UTC) == event_created_by_user_with_place.address.created
        assert datetime.datetime.strptime(
            address.get('updated'), '%Y-%m-%dT%H:%M:%S.%fZ'
        ).replace(tzinfo=pytz.UTC) == event_created_by_user_with_place.address.updated

        assert datetime.datetime.strptime(
            event_dict.get('date'), '%Y-%m-%dT%H:%M:%SZ'
        ).replace(tzinfo=pytz.UTC) == event_created_by_user_with_place.date
        assert event_dict.get('duration') == event_created_by_user_with_place.duration
        assert event_dict.get('age_rate') == event_created_by_user_with_place.age_rate
        assert event_dict.get('is_approved') == event_created_by_user_with_place.is_approved
        assert event_dict.get('is_hot') == event_created_by_user_with_place.is_hot
        assert event_dict.get('is_top') == event_created_by_user_with_place.is_top
        assert event_dict.get('max_members') == event_created_by_user_with_place.max_members
        assert event_dict.get('status') == event_created_by_user_with_place.status
        assert datetime.datetime.strptime(
            event_dict.get('created'), '%Y-%m-%dT%H:%M:%S.%fZ'
        ).replace(tzinfo=pytz.UTC) == event_created_by_user_with_place.created
        assert datetime.datetime.strptime(
            event_dict.get('updated'), '%Y-%m-%dT%H:%M:%S.%fZ'
        ).replace(tzinfo=pytz.UTC) == event_created_by_user_with_place.updated

    def test_detail_event_by_organization_without_place(self, client, event_created_by_organization_without_place):
        """Test event created by user without place"""
        res = client.get(f'/api/events/{event_created_by_organization_without_place.id}/')
        assert res.status_code == status.HTTP_200_OK
        event_dict = res.json()
        assert event_dict.get('name') == event_created_by_organization_without_place.name
        assert event_dict.get('description') == event_created_by_organization_without_place.description
        assert event_dict.get('poster') == event_created_by_organization_without_place.poster
        assert event_dict.get('organizer_id') == str(event_created_by_organization_without_place.organizer_id)
        assert event_dict.get('organizer_type') == str(
            event_created_by_organization_without_place.organizer_type).title()

        organizer = event_dict.get('organizer')
        assert organizer
        assert organizer.get('id') == str(event_created_by_organization_without_place.organizer.id)
        assert organizer.get('name') == event_created_by_organization_without_place.organizer.name
        assert organizer.get('email') == event_created_by_organization_without_place.organizer.email

        address = event_dict.get('address')
        assert address
        assert address.get('id') == str(event_created_by_organization_without_place.address.id)
        assert address.get('country') == event_created_by_organization_without_place.address.country
        assert address.get('city') == event_created_by_organization_without_place.address.city
        assert address.get('street') == event_created_by_organization_without_place.address.street
        assert address.get('house') == event_created_by_organization_without_place.address.house
        assert address.get('floor') == event_created_by_organization_without_place.address.floor
        assert address.get('apartments') == event_created_by_organization_without_place.address.apartments
        assert address.get('description') == event_created_by_organization_without_place.address.description
        assert datetime.datetime.strptime(
            address.get('created'), '%Y-%m-%dT%H:%M:%S.%fZ'
        ).replace(tzinfo=pytz.UTC) == event_created_by_organization_without_place.address.created
        assert datetime.datetime.strptime(
            address.get('updated'), '%Y-%m-%dT%H:%M:%S.%fZ'
        ).replace(tzinfo=pytz.UTC) == event_created_by_organization_without_place.address.updated

        assert datetime.datetime.strptime(
            event_dict.get('date'), '%Y-%m-%dT%H:%M:%SZ'
        ).replace(tzinfo=pytz.UTC) == event_created_by_organization_without_place.date
        assert event_dict.get('duration') == event_created_by_organization_without_place.duration
        assert event_dict.get('age_rate') == event_created_by_organization_without_place.age_rate
        assert event_dict.get('is_approved') == event_created_by_organization_without_place.is_approved
        assert event_dict.get('is_hot') == event_created_by_organization_without_place.is_hot
        assert event_dict.get('is_top') == event_created_by_organization_without_place.is_top
        assert event_dict.get('max_members') == event_created_by_organization_without_place.max_members
        assert event_dict.get('status') == event_created_by_organization_without_place.status
        assert datetime.datetime.strptime(
            event_dict.get('created'), '%Y-%m-%dT%H:%M:%S.%fZ'
        ).replace(tzinfo=pytz.UTC) == event_created_by_organization_without_place.created
        assert datetime.datetime.strptime(
            event_dict.get('updated'), '%Y-%m-%dT%H:%M:%S.%fZ'
        ).replace(tzinfo=pytz.UTC) == event_created_by_organization_without_place.updated

    def test_detail_event_by_organization_with_place(self, client, event_created_by_organization_with_place):
        res = client.get(f'/api/events/{event_created_by_organization_with_place.id}/')
        assert res.status_code == status.HTTP_200_OK
        event_dict = res.json()
        assert event_dict.get('name') == event_created_by_organization_with_place.name
        assert event_dict.get('description') == event_created_by_organization_with_place.description
        assert event_dict.get('poster') == event_created_by_organization_with_place.poster
        assert event_dict.get('organizer_id') == str(event_created_by_organization_with_place.organizer_id)
        assert event_dict.get('organizer_type') == str(event_created_by_organization_with_place.organizer_type).title()

        organizer = event_dict.get('organizer')
        assert organizer
        assert organizer.get('id') == str(event_created_by_organization_with_place.organizer.id)
        assert organizer.get('name') == event_created_by_organization_with_place.organizer.name
        assert organizer.get('email') == event_created_by_organization_with_place.organizer.email

        place = event_dict.get('place')
        assert place
        assert place.get('id') == str(event_created_by_organization_with_place.place.id)
        assert place.get('name') == event_created_by_organization_with_place.place.name
        assert place.get('description') == event_created_by_organization_with_place.place.description
        assert datetime.datetime.strptime(
            place.get('created'), '%Y-%m-%dT%H:%M:%S.%fZ'
        ).replace(tzinfo=pytz.UTC) == event_created_by_organization_with_place.place.created
        assert place.get('status') == event_created_by_organization_with_place.place.status

        address = event_dict.get('address')
        assert address
        assert address.get('id') == str(event_created_by_organization_with_place.address.id)
        assert address.get('country') == event_created_by_organization_with_place.address.country
        assert address.get('city') == event_created_by_organization_with_place.address.city
        assert address.get('street') == event_created_by_organization_with_place.address.street
        assert address.get('house') == event_created_by_organization_with_place.address.house
        assert address.get('floor') == event_created_by_organization_with_place.address.floor
        assert address.get('apartments') == event_created_by_organization_with_place.address.apartments
        assert address.get('description') == event_created_by_organization_with_place.address.description
        assert datetime.datetime.strptime(
            address.get('created'), '%Y-%m-%dT%H:%M:%S.%fZ'
        ).replace(tzinfo=pytz.UTC) == event_created_by_organization_with_place.address.created
        assert datetime.datetime.strptime(
            address.get('updated'), '%Y-%m-%dT%H:%M:%S.%fZ'
        ).replace(tzinfo=pytz.UTC) == event_created_by_organization_with_place.address.updated

        assert datetime.datetime.strptime(
            event_dict.get('date'), '%Y-%m-%dT%H:%M:%SZ'
        ).replace(tzinfo=pytz.UTC) == event_created_by_organization_with_place.date
        assert event_dict.get('duration') == event_created_by_organization_with_place.duration
        assert event_dict.get('age_rate') == event_created_by_organization_with_place.age_rate
        assert event_dict.get('is_approved') == event_created_by_organization_with_place.is_approved
        assert event_dict.get('is_hot') == event_created_by_organization_with_place.is_hot
        assert event_dict.get('is_top') == event_created_by_organization_with_place.is_top
        assert event_dict.get('max_members') == event_created_by_organization_with_place.max_members
        assert event_dict.get('status') == event_created_by_organization_with_place.status
        assert datetime.datetime.strptime(
            event_dict.get('created'), '%Y-%m-%dT%H:%M:%S.%fZ'
        ).replace(tzinfo=pytz.UTC) == event_created_by_organization_with_place.created
        assert datetime.datetime.strptime(
            event_dict.get('updated'), '%Y-%m-%dT%H:%M:%S.%fZ'
        ).replace(tzinfo=pytz.UTC) == event_created_by_organization_with_place.updated

    def test_detail_negative(self, client):
        """Negative test checks access to uncreated event by random uuid"""
        res = client.get(f'/api/events/{faker.Faker().uuid4()}/')
        assert res.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.parametrize('event_qty', [0, 1, 10, 50])
    def test_list_user_without_place(self, client, events_user_without_place, event_qty):
        """Collection of events created by user with place"""
        res = client.get(f'/api/events/')
        assert res.status_code == status.HTTP_200_OK
        assert isinstance(res.json(), list)
        assert len(res.json()) == event_qty

    @pytest.mark.parametrize('event_qty', [0, 1, 10, 50])
    def test_list_user_with_place(self, client, events_user_with_pace, event_qty):
        res = client.get(f'/api/events/')
        assert res.status_code == status.HTTP_200_OK
        assert isinstance(res.json(), list)
        assert len(res.json()) == event_qty

    @pytest.mark.parametrize('event_qty', [0, 1, 10, 50])
    def test_list_org_without_place(self, client, events_org_without_place, event_qty):
        res = client.get(f'/api/events/')
        assert res.status_code == status.HTTP_200_OK
        assert isinstance(res.json(), list)
        assert len(res.json()) == event_qty

    @pytest.mark.parametrize('event_qty', [0, 1, 10, 50])
    def test_list_org_with_place(self, client, events_org_with_place, event_qty):
        res = client.get(f'/api/events/')
        assert res.status_code == status.HTTP_200_OK
        assert isinstance(res.json(), list)
        assert len(res.json()) == event_qty

    @pytest.mark.parametrize('ordering', ['created', '-created'])
    @pytest.mark.parametrize('event_qty', [16, 20, 40])
    def test_list_ordering(self, client, events_batch_for_filtering_and_ordering, event_qty, ordering):
        res = client.get(f'/api/events/?ordering={ordering}')
        assert res.status_code == status.HTTP_200_OK
        assert isinstance(res.json(), list)
        assert len(res.json()) == event_qty
        event_list = Event.objects.all().order_by(ordering).values_list('id', flat=True)
        for i in range(event_qty):
            assert res.json()[i].get('id') == str(event_list[i])

    @pytest.mark.parametrize('filtering', ['place', 'address', 'organizer', 'date__lte', 'date__gte'])
    @pytest.mark.parametrize('event_qty', [8, 16])
    def test_list_filtering_non_bool_vals(self, client, events_batch_for_filtering_and_ordering, event_qty, filtering):
        data = None
        event_list = []
        if filtering == 'place':
            data = Place.objects.all()[0].id
            event_list = Event.objects.filter(place_id=data).values_list('id', flat=True).order_by('created')
        elif filtering == 'address':
            data = Event.objects.all()[0].address_id
            event_list = Event.objects.filter(address_id=data).values_list('id', flat=True).order_by('created')
        elif filtering == 'organizer':
            data = Event.objects.all()[event_qty//2].organizer_id
            event_list = Event.objects.filter(organizer_id=data).values_list('id', flat=True).order_by('created')
        elif filtering.endswith('lte'):
            data = '2019-09-10 12:00'
            event_list = Event.objects.filter(date__lte=data).values_list('id', flat=True).order_by('created')
        elif filtering.endswith('gte'):
            data = '2019-09-10 12:00'
            event_list = Event.objects.filter(date__gte=data).values_list('id', flat=True).order_by('created')
        res = client.get(f'/api/events/?{filtering}={data}&ordering=created')
        assert res.status_code == status.HTTP_200_OK
        assert isinstance(res.json(), list)
        for i in range(len(res.json())):
            assert res.json()[i].get('id') == str(event_list[i])

    @pytest.mark.parametrize('data', [True, False])
    @pytest.mark.parametrize('filtering', ['is_top', 'is_hot'])
    @pytest.mark.parametrize('event_qty', [8, 16])
    def test_list_filtering_bool_vals(self, client, events_batch_for_filtering_and_ordering, event_qty, filtering, data):
        event_list = []
        if filtering.endswith('top'):
            event_list = Event.objects.filter(is_top=data).values_list('id', flat=True).order_by('created')
        elif filtering.endswith('hot'):
            event_list = Event.objects.filter(is_hot=data).values_list('id', flat=True).order_by('created')
        res = client.get(f'/api/events/?{filtering}={data}&ordering=created')
        assert res.status_code == status.HTTP_200_OK
        assert isinstance(res.json(), list)
        for i in range(len(res.json())):
            assert res.json()[0].get('id') == str(event_list[0])


@pytest.mark.django_db
class TestEventsCreate:
    """
    Tests which imitates create() for events
    """

    def test_create_event_not_authenticated_user(self, client, user, event_dict, address_dict):
        event_dict.update(address=address_dict)
        res = client.post('/api/events/', data=json.dumps(event_dict),
                          content_type='application/json')
        assert res.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_event_with_not_allowed_to_specify_fields(self, client, user, token, event_dict, address_dict):
        event_dict.update(address=address_dict)
        res = client.post('/api/events/', data=json.dumps(event_dict),
                          content_type='application/json',
                          **{'HTTP_AUTHORIZATION': 'Token ' + str(token)})
        assert res.status_code == status.HTTP_201_CREATED
        res_event = res.json()
        assert res_event.get('id')
        db_event = Event.objects.get(id=res_event.get('id'))
        assert db_event.name == res_event.get('name')
        assert db_event.description == res_event.get('description')
        assert bool(db_event.poster) == bool(res_event.get('poster'))
        assert db_event.date == datetime.datetime.strptime(res_event.get('date'),
                                                           '%Y-%m-%dT%H:%M:%SZ'
                                                           ).replace(tzinfo=pytz.UTC)
        assert str(db_event.duration) == res_event.get('duration')
        assert db_event.created == datetime.datetime.strptime(res_event.get('created'),
                                                              '%Y-%m-%dT%H:%M:%S.%fZ'
                                                              ).replace(tzinfo=pytz.UTC)
        assert db_event.created == datetime.datetime.strptime(res_event.get('created'),
                                                              '%Y-%m-%dT%H:%M:%S.%fZ'
                                                              ).replace(tzinfo=pytz.UTC)
        assert db_event.updated == datetime.datetime.strptime(res_event.get('updated'),
                                                              '%Y-%m-%dT%H:%M:%S.%fZ'
                                                              ).replace(tzinfo=pytz.UTC)
        assert db_event.age_rate == res_event.get('age_rate')
        assert db_event.max_members == res_event.get('max_members')
        assert db_event.status == Event.SOON
        assert db_event.is_approved == res_event.get('is_approved')
        assert db_event.is_hot == res_event.get('is_hot')
        assert db_event.is_top == res_event.get('is_top')
        assert str(db_event.address.id) == res_event.get('address').get('id')

    def test_create_event_with_empty_place_and_address_id_in_dict(self, client, user, address, token, event_dict):
        address = Address.objects.first()
        address_id = {
            'id': str(address.id)
        }
        event_dict.pop('place')
        event_dict.update(address=address_id)
        res = client.post('/api/events/', data=json.dumps(event_dict),
                          content_type='application/json',
                          **{'HTTP_AUTHORIZATION': 'Token ' + str(token)})
        assert res.status_code == status.HTTP_201_CREATED
        res_event = res.json()
        assert res_event.get('id')
        db_event = Event.objects.get(id=res_event.get('id'))
        assert db_event.name == res_event.get('name')
        assert db_event.description == res_event.get('description')
        assert bool(db_event.poster) == bool(res_event.get('poster'))
        assert db_event.date == datetime.datetime.strptime(res_event.get('date'),
                                                           '%Y-%m-%dT%H:%M:%SZ'
                                                           ).replace(tzinfo=pytz.UTC)
        assert str(db_event.duration) == res_event.get('duration')
        assert db_event.created == datetime.datetime.strptime(res_event.get('created'),
                                                              '%Y-%m-%dT%H:%M:%S.%fZ'
                                                              ).replace(tzinfo=pytz.UTC)
        assert db_event.created == datetime.datetime.strptime(res_event.get('created'),
                                                              '%Y-%m-%dT%H:%M:%S.%fZ'
                                                              ).replace(tzinfo=pytz.UTC)
        assert db_event.updated == datetime.datetime.strptime(res_event.get('updated'),
                                                              '%Y-%m-%dT%H:%M:%S.%fZ'
                                                              ).replace(tzinfo=pytz.UTC)
        assert db_event.age_rate == res_event.get('age_rate')
        assert db_event.max_members == res_event.get('max_members')
        assert str(db_event.address.id) == res_event.get('address').get('id')

    def test_create_event_with_empty_place_and_address_id_in_str(self, client, user, address, token, event_dict):
        address = Address.objects.first()
        event_dict.pop('place')
        event_dict.update(address=str(address.id))
        res = client.post('/api/events/', data=json.dumps(event_dict),
                          content_type='application/json',
                          **{'HTTP_AUTHORIZATION': 'Token ' + str(token)})
        assert res.status_code == status.HTTP_201_CREATED
        res_event = res.json()
        assert res_event.get('id')
        db_event = Event.objects.get(id=res_event.get('id'))
        assert db_event.name == res_event.get('name')
        assert db_event.description == res_event.get('description')
        assert bool(db_event.poster) == bool(res_event.get('poster'))
        assert db_event.date == datetime.datetime.strptime(res_event.get('date'),
                                                           '%Y-%m-%dT%H:%M:%SZ'
                                                           ).replace(tzinfo=pytz.UTC)
        assert str(db_event.duration) == res_event.get('duration')
        assert db_event.created == datetime.datetime.strptime(res_event.get('created'),
                                                              '%Y-%m-%dT%H:%M:%S.%fZ'
                                                              ).replace(tzinfo=pytz.UTC)
        assert db_event.created == datetime.datetime.strptime(res_event.get('created'),
                                                              '%Y-%m-%dT%H:%M:%S.%fZ'
                                                              ).replace(tzinfo=pytz.UTC)
        assert db_event.updated == datetime.datetime.strptime(res_event.get('updated'),
                                                              '%Y-%m-%dT%H:%M:%S.%fZ'
                                                              ).replace(tzinfo=pytz.UTC)
        assert db_event.age_rate == res_event.get('age_rate')
        assert db_event.max_members == res_event.get('max_members')
        assert str(db_event.address.id) == res_event.get('address').get('id')

    def test_create_event_with_place_none_and_address_id_in_dict(self, client, user, address, token, event_dict):
        address = Address.objects.first()
        address_id = {
            'id': str(address.id)
        }
        event_dict.update(address=address_id)
        res = client.post('/api/events/', data=json.dumps(event_dict),
                          content_type='application/json',
                          **{'HTTP_AUTHORIZATION': 'Token ' + str(token)})
        assert res.status_code == status.HTTP_201_CREATED
        res_event = res.json()
        assert res_event.get('id')
        db_event = Event.objects.get(id=res_event.get('id'))
        assert db_event.name == res_event.get('name')
        assert db_event.description == res_event.get('description')
        assert bool(db_event.poster) == bool(res_event.get('poster'))
        assert db_event.date == datetime.datetime.strptime(res_event.get('date'),
                                                           '%Y-%m-%dT%H:%M:%SZ'
                                                           ).replace(tzinfo=pytz.UTC)
        assert str(db_event.duration) == res_event.get('duration')
        assert db_event.created == datetime.datetime.strptime(res_event.get('created'),
                                                              '%Y-%m-%dT%H:%M:%S.%fZ'
                                                              ).replace(tzinfo=pytz.UTC)
        assert db_event.created == datetime.datetime.strptime(res_event.get('created'),
                                                              '%Y-%m-%dT%H:%M:%S.%fZ'
                                                              ).replace(tzinfo=pytz.UTC)
        assert db_event.updated == datetime.datetime.strptime(res_event.get('updated'),
                                                              '%Y-%m-%dT%H:%M:%S.%fZ'
                                                              ).replace(tzinfo=pytz.UTC)
        assert db_event.age_rate == res_event.get('age_rate')
        assert db_event.max_members == res_event.get('max_members')
        assert str(db_event.address.id) == res_event.get('address').get('id')

    def test_create_event_with_place_none_and_address_id_in_str(self, client, user, address, token, event_dict):
        address = Address.objects.first()
        event_dict.update(address=str(address.id))
        res = client.post('/api/events/', data=json.dumps(event_dict),
                          content_type='application/json',
                          **{'HTTP_AUTHORIZATION': 'Token ' + str(token)})
        assert res.status_code == status.HTTP_201_CREATED
        res_event = res.json()
        assert res_event.get('id')
        db_event = Event.objects.get(id=res_event.get('id'))
        assert db_event.name == res_event.get('name')
        assert db_event.description == res_event.get('description')
        assert bool(db_event.poster) == bool(res_event.get('poster'))
        assert db_event.date == datetime.datetime.strptime(res_event.get('date'),
                                                           '%Y-%m-%dT%H:%M:%SZ'
                                                           ).replace(tzinfo=pytz.UTC)
        assert str(db_event.duration) == res_event.get('duration')
        assert db_event.created == datetime.datetime.strptime(res_event.get('created'),
                                                              '%Y-%m-%dT%H:%M:%S.%fZ'
                                                              ).replace(tzinfo=pytz.UTC)
        assert db_event.created == datetime.datetime.strptime(res_event.get('created'),
                                                              '%Y-%m-%dT%H:%M:%S.%fZ'
                                                              ).replace(tzinfo=pytz.UTC)
        assert db_event.updated == datetime.datetime.strptime(res_event.get('updated'),
                                                              '%Y-%m-%dT%H:%M:%S.%fZ'
                                                              ).replace(tzinfo=pytz.UTC)
        assert db_event.age_rate == res_event.get('age_rate')
        assert db_event.max_members == res_event.get('max_members')
        assert str(db_event.address.id) == res_event.get('address').get('id')

    def test_create_event_with_empty_place_and_new_address(self, client, user, token, event_dict, address_dict):
        event_dict.update(address=address_dict)
        event_dict.pop('place')
        res = client.post('/api/events/', data=json.dumps(event_dict),
                          content_type='application/json',
                          **{'HTTP_AUTHORIZATION': 'Token ' + str(token)})
        assert res.status_code == status.HTTP_201_CREATED
        res_event = res.json()
        assert res_event.get('id')
        db_event = Event.objects.get(id=res_event.get('id'))
        assert db_event.name == res_event.get('name')
        assert db_event.description == res_event.get('description')
        assert bool(db_event.poster) == bool(res_event.get('poster'))
        assert db_event.date == datetime.datetime.strptime(res_event.get('date'),
                                                           '%Y-%m-%dT%H:%M:%SZ'
                                                           ).replace(tzinfo=pytz.UTC)
        assert str(db_event.duration) == res_event.get('duration')
        assert db_event.created == datetime.datetime.strptime(res_event.get('created'),
                                                              '%Y-%m-%dT%H:%M:%S.%fZ'
                                                              ).replace(tzinfo=pytz.UTC)
        assert db_event.created == datetime.datetime.strptime(res_event.get('created'),
                                                              '%Y-%m-%dT%H:%M:%S.%fZ'
                                                              ).replace(tzinfo=pytz.UTC)
        assert db_event.updated == datetime.datetime.strptime(res_event.get('updated'),
                                                              '%Y-%m-%dT%H:%M:%S.%fZ'
                                                              ).replace(tzinfo=pytz.UTC)
        assert db_event.age_rate == res_event.get('age_rate')
        assert db_event.max_members == res_event.get('max_members')
        assert str(db_event.address.id) == res_event.get('address').get('id')

    def test_create_event_with_place_none_and_new_address(self, client, user, token, event_dict, address_dict):
        event_dict.update(address=address_dict)
        res = client.post('/api/events/', data=json.dumps(event_dict),
                          content_type='application/json',
                          **{'HTTP_AUTHORIZATION': 'Token ' + str(token)})
        assert res.status_code == status.HTTP_201_CREATED
        res_event = res.json()
        assert res_event.get('id')
        db_event = Event.objects.get(id=res_event.get('id'))
        assert db_event.name == res_event.get('name')
        assert db_event.description == res_event.get('description')
        assert bool(db_event.poster) == bool(res_event.get('poster'))
        assert db_event.date == datetime.datetime.strptime(res_event.get('date'),
                                                           '%Y-%m-%dT%H:%M:%SZ'
                                                           ).replace(tzinfo=pytz.UTC)
        assert str(db_event.duration) == res_event.get('duration')
        assert db_event.created == datetime.datetime.strptime(res_event.get('created'),
                                                              '%Y-%m-%dT%H:%M:%S.%fZ'
                                                              ).replace(tzinfo=pytz.UTC)
        assert db_event.created == datetime.datetime.strptime(res_event.get('created'),
                                                              '%Y-%m-%dT%H:%M:%S.%fZ'
                                                              ).replace(tzinfo=pytz.UTC)
        assert db_event.updated == datetime.datetime.strptime(res_event.get('updated'),
                                                              '%Y-%m-%dT%H:%M:%S.%fZ'
                                                              ).replace(tzinfo=pytz.UTC)
        assert db_event.age_rate == res_event.get('age_rate')
        assert db_event.max_members == res_event.get('max_members')
        assert str(db_event.address.id) == res_event.get('address').get('id')

    def test_create_event_with_place_id_in_str_and_any_address_data(self, client, user, token, place, event_dict,
                                                                    address_dict):
        place = Place.objects.first()
        event_dict.update(place=str(place.id))
        event_dict.update(address=address_dict)
        res = client.post('/api/events/', data=json.dumps(event_dict),
                          content_type='application/json',
                          **{'HTTP_AUTHORIZATION': 'Token ' + str(token)})
        assert res.status_code == status.HTTP_201_CREATED
        res_event = res.json()
        assert res_event.get('id')
        db_event = Event.objects.get(id=res_event.get('id'))
        assert db_event.name == res_event.get('name')
        assert db_event.description == res_event.get('description')
        assert bool(db_event.poster) == bool(res_event.get('poster'))
        assert db_event.date == datetime.datetime.strptime(res_event.get('date'),
                                                           '%Y-%m-%dT%H:%M:%SZ'
                                                           ).replace(tzinfo=pytz.UTC)
        assert str(db_event.duration) == res_event.get('duration')
        assert db_event.created == datetime.datetime.strptime(res_event.get('created'),
                                                              '%Y-%m-%dT%H:%M:%S.%fZ'
                                                              ).replace(tzinfo=pytz.UTC)
        assert db_event.created == datetime.datetime.strptime(res_event.get('created'),
                                                              '%Y-%m-%dT%H:%M:%S.%fZ'
                                                              ).replace(tzinfo=pytz.UTC)
        assert db_event.updated == datetime.datetime.strptime(res_event.get('updated'),
                                                              '%Y-%m-%dT%H:%M:%S.%fZ'
                                                              ).replace(tzinfo=pytz.UTC)
        assert db_event.age_rate == res_event.get('age_rate')
        assert db_event.max_members == res_event.get('max_members')
        assert str(db_event.address.id) == res_event.get('address').get('id')
        assert str(db_event.place.id) == res_event.get('place').get('id')

    def test_create_event_with_place_id_in_dict_and_any_address_data(self, client, user, token, place, event_dict,
                                                                     address_dict):
        place = Place.objects.first()
        place_id = {
            'id': str(place.id)
        }
        event_dict.update(place=place_id)
        event_dict.update(address=address_dict)
        res = client.post('/api/events/', data=json.dumps(event_dict),
                          content_type='application/json',
                          **{'HTTP_AUTHORIZATION': 'Token ' + str(token)})
        assert res.status_code == status.HTTP_201_CREATED
        res_event = res.json()
        assert res_event.get('id')
        db_event = Event.objects.get(id=res_event.get('id'))
        assert db_event.name == res_event.get('name')
        assert db_event.description == res_event.get('description')
        assert bool(db_event.poster) == bool(res_event.get('poster'))
        assert db_event.date == datetime.datetime.strptime(res_event.get('date'),
                                                           '%Y-%m-%dT%H:%M:%SZ'
                                                           ).replace(tzinfo=pytz.UTC)
        assert str(db_event.duration) == res_event.get('duration')
        assert db_event.created == datetime.datetime.strptime(res_event.get('created'),
                                                              '%Y-%m-%dT%H:%M:%S.%fZ'
                                                              ).replace(tzinfo=pytz.UTC)
        assert db_event.created == datetime.datetime.strptime(res_event.get('created'),
                                                              '%Y-%m-%dT%H:%M:%S.%fZ'
                                                              ).replace(tzinfo=pytz.UTC)
        assert db_event.updated == datetime.datetime.strptime(res_event.get('updated'),
                                                              '%Y-%m-%dT%H:%M:%S.%fZ'
                                                              ).replace(tzinfo=pytz.UTC)
        assert db_event.age_rate == res_event.get('age_rate')
        assert db_event.max_members == res_event.get('max_members')
        assert str(db_event.address.id) == res_event.get('address').get('id')
        assert str(db_event.place.id) == res_event.get('place').get('id')
