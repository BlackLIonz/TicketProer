import pytest
from pytest_factoryboy import register

from apps.events.factories import (
    EventUserWithoutPlaceFactory,
    EventUserWithPlaceFactory,
    EventOrganizerWithoutPlaceFactory,
    EventOrganizerWithPlaceFactory
)
from apps.locations.factories import AddressFactory, PlaceFactory
from apps.users.factories import UserFactory, OrganizationFactory

register(UserFactory, 'user')
register(PlaceFactory, 'place')
register(AddressFactory, 'address')
register(OrganizationFactory, 'organization')
register(EventUserWithoutPlaceFactory, 'event_created_by_user_without_place')
register(EventUserWithPlaceFactory, 'event_created_by_user_with_place')
register(EventOrganizerWithoutPlaceFactory, 'event_created_by_organization_without_place')
register(EventOrganizerWithPlaceFactory, 'event_created_by_organization_with_place')


@pytest.fixture
def event_qty():
    return 1


@pytest.fixture
def events_user_without_place(event_qty):
    return EventUserWithoutPlaceFactory.create_batch(size=event_qty)


@pytest.fixture
def events_user_with_pace(event_qty):
    return EventUserWithPlaceFactory.create_batch(size=event_qty)


@pytest.fixture
def events_org_without_place(event_qty):
    return EventOrganizerWithoutPlaceFactory.create_batch(size=event_qty)


@pytest.fixture
def events_org_with_place(event_qty):
    return EventOrganizerWithPlaceFactory.create_batch(size=event_qty)
