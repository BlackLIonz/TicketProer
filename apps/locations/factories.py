import random

import factory
import factory.fuzzy

from faker import Factory as FakeFactory

from apps.locations.models import Address, Place


faker = FakeFactory.create()


class AddressFactory(factory.django.DjangoModelFactory):
    """Address factory"""
    country = factory.LazyAttribute(lambda x: faker.country()[:30])
    city = factory.LazyAttribute(lambda x: faker.city()[:30])
    street = factory.LazyAttribute(lambda x: faker.street_name()[:30])
    house = factory.LazyAttribute(lambda x: faker.building_number()[:10])
    floor = factory.LazyAttribute(lambda x: random.randint(1, 50))
    apartments = factory.LazyAttribute(lambda x: random.randint(1, 1000))

    class Meta:
        model = Address
        abstract = False


class PlaceFactory(factory.django.DjangoModelFactory):
    """Place factory"""
    name = factory.LazyAttribute(lambda x: faker.company()[:75])
    address = factory.SubFactory(AddressFactory)
    description = factory.Faker('text', max_nb_chars=200, ext_word_list=None)
    status = factory.fuzzy.FuzzyChoice(Place.STATUS_CHOICES, getter=lambda c: c[0])

    class Meta:
        model = Place
        abstract = False
