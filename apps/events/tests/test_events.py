import datetime

import faker
import pytz
import pytest
from rest_framework import status


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
                    event_dict.get('date'), '%Y-%m-%dT%H:%M:%SZ'
               ).replace(tzinfo=pytz.UTC) == event_created_by_user_without_place.date
        assert event_dict.get('duration') == event_created_by_user_without_place.duration
        assert event_dict.get('age_rate') == event_created_by_user_without_place.age_rate
        assert event_dict.get('is_approved') == event_created_by_user_without_place.is_approved
        assert event_dict.get('is_hot') == event_created_by_user_without_place.is_hot
        assert event_dict.get('is_top') == event_created_by_user_without_place.is_top
        assert event_dict.get('max_members') == event_created_by_user_without_place.max_members
        assert event_dict.get('status') == event_created_by_user_without_place.status

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
                    event_dict.get('date'), '%Y-%m-%dT%H:%M:%SZ'
               ).replace(tzinfo=pytz.UTC) == event_created_by_user_with_place.date
        assert event_dict.get('duration') == event_created_by_user_with_place.duration
        assert event_dict.get('age_rate') == event_created_by_user_with_place.age_rate
        assert event_dict.get('is_approved') == event_created_by_user_with_place.is_approved
        assert event_dict.get('is_hot') == event_created_by_user_with_place.is_hot
        assert event_dict.get('is_top') == event_created_by_user_with_place.is_top
        assert event_dict.get('max_members') == event_created_by_user_with_place.max_members
        assert event_dict.get('status') == event_created_by_user_with_place.status

    def test_detail_event_by_organization_without_place(self, client, event_created_by_organization_without_place):
        """Test event created by user without place"""
        res = client.get(f'/api/events/{event_created_by_organization_without_place.id}/')
        assert res.status_code == status.HTTP_200_OK
        event_dict = res.json()
        assert event_dict.get('name') == event_created_by_organization_without_place.name
        assert event_dict.get('description') == event_created_by_organization_without_place.description
        assert event_dict.get('poster') == event_created_by_organization_without_place.poster
        assert event_dict.get('organizer_id') == str(event_created_by_organization_without_place.organizer_id)
        assert event_dict.get('organizer_type') == str(event_created_by_organization_without_place.organizer_type).title()

        organizer = event_dict.get('organizer')
        assert organizer
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
                    event_dict.get('date'), '%Y-%m-%dT%H:%M:%SZ'
               ).replace(tzinfo=pytz.UTC) == event_created_by_organization_without_place.date
        assert event_dict.get('duration') == event_created_by_organization_without_place.duration
        assert event_dict.get('age_rate') == event_created_by_organization_without_place.age_rate
        assert event_dict.get('is_approved') == event_created_by_organization_without_place.is_approved
        assert event_dict.get('is_hot') == event_created_by_organization_without_place.is_hot
        assert event_dict.get('is_top') == event_created_by_organization_without_place.is_top
        assert event_dict.get('max_members') == event_created_by_organization_without_place.max_members
        assert event_dict.get('status') == event_created_by_organization_without_place.status

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
                    event_dict.get('date'), '%Y-%m-%dT%H:%M:%SZ'
               ).replace(tzinfo=pytz.UTC) == event_created_by_organization_with_place.date
        assert event_dict.get('duration') == event_created_by_organization_with_place.duration
        assert event_dict.get('age_rate') == event_created_by_organization_with_place.age_rate
        assert event_dict.get('is_approved') == event_created_by_organization_with_place.is_approved
        assert event_dict.get('is_hot') == event_created_by_organization_with_place.is_hot
        assert event_dict.get('is_top') == event_created_by_organization_with_place.is_top
        assert event_dict.get('max_members') == event_created_by_organization_with_place.max_members
        assert event_dict.get('status') == event_created_by_organization_with_place.status

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
