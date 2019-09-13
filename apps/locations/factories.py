import random

import factory

from faker import Factory as FakeFactory

from apps.locations.models import Address
from apps.users.factories import UserFactory

faker = FakeFactory.create()


class AddressFactory(factory.django.DjangoModelFactory):
    """Address factory"""
    country = factory.LazyAttribute(lambda x: faker.country()[:30])
    city = factory.LazyAttribute(lambda x: faker.city()[:30])
    street = factory.LazyAttribute(lambda x: faker.street_name()[:30])
    house = factory.LazyAttribute(lambda x: faker.building_number()[:10])
    floor = factory.LazyAttribute(lambda x: random.randint(1, 50))
    apartments = factory.LazyAttribute(lambda x: random.randint(1, 1000))
    created_by = factory.SubFactory(UserFactory)

    class Meta:
        model = Address
        abstract = False
