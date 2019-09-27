import factory
from faker import Factory as FakeFactory

from apps.users.models import User, Organization, MembersList

faker = FakeFactory.create()


class UserFactory(factory.django.DjangoModelFactory):
    username = factory.Faker('user_name')
    password = factory.Faker('password')
    email = factory.Faker('email')
    date_of_birth = factory.Faker('date_of_birth')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')

    class Meta:
        model = User


class OrganizationFactory(factory.django.DjangoModelFactory):
    name = factory.Faker('company')
    email = factory.Faker('email')
    approved = factory.Faker('boolean', chance_of_getting_true=60)
    description = factory.Faker('text', max_nb_chars=200, ext_word_list=None)

    class Meta:
        model = Organization


class MemberListFactory(factory.django.DjangoModelFactory):
    member = factory.SubFactory(UserFactory)
    organization = factory.Iterator(Organization.objects.filter(membership__isnull=True))

    class Meta:
        model = MembersList
