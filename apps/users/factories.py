from apps.users.models import User

import factory
from faker import Factory as FakeFactory

faker = FakeFactory.create()


class UserFactory(factory.django.DjangoModelFactory):
    """User factory"""
    username = factory.LazyAttribute(lambda x: faker.user_name())
    password = factory.LazyAttribute(lambda x: faker.password())
    email = factory.LazyAttribute(lambda x: faker.email())
    date_of_birth = factory.LazyAttribute(lambda x: faker.date_of_birth())
    first_name = factory.LazyAttribute(lambda x: faker.first_name())
    last_name = factory.LazyAttribute(lambda x: faker.last_name())

    class Meta:
        model = User
        abstract = False
