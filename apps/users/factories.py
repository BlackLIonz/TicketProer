import factory

from faker import Factory as FakeFactory

from apps.users.models import User, Organization, MembersList


faker = FakeFactory.create()


class UserFactory(factory.django.DjangoModelFactory):
    """User factory"""
    username = factory.Faker('user_name')
    password = factory.Faker('password')
    email = factory.Faker('email')
    date_of_birth = factory.Faker('date_of_birth')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')

    class Meta:
        model = User
        abstract = False


class OrganizationFactory(factory.django.DjangoModelFactory):
    """Organization factory"""
    name = factory.Faker('company')
    email = factory.Faker('email')
    approved = factory.Faker('boolean', chance_of_getting_true=60)
    description = factory.Faker('text', max_nb_chars=200, ext_word_list=None)

    class Meta:
        model = Organization
        abstract = False


class MemberListFactory(factory.django.DjangoModelFactory):
    """Organization and user connection"""
    member = factory.SubFactory(UserFactory)
    organization = factory.SubFactory(OrganizationFactory)

    class Meta:
        model = MembersList
        abstract = False
