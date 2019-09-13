import factory
import factory.fuzzy

from faker import Factory as FakeFactory
from django.contrib.contenttypes.models import ContentType

from apps.users.models import Organization
from apps.events.models import Event

from apps.users.factories import UserFactory, MemberListFactory
from apps.locations.factories import AddressFactory, PlaceFactory


faker = FakeFactory.create()


class EventAbstractFactory(factory.django.DjangoModelFactory):
    """Abstract Event factory"""
    name = factory.LazyAttribute(lambda x: faker.catch_phrase()[:64])
    description = factory.Faker('text', max_nb_chars=200, ext_word_list=None)
    organizer_id = factory.SelfAttribute('organizer.id')
    organizer_type = factory.LazyAttribute(
        lambda o: ContentType.objects.get_for_model(o.organizer)
    )
    date = factory.Faker('past_datetime', start_date='-30d')
    duration = factory.Faker('time')
    age_rate = factory.Faker('pyint', min_value=0, max_value=50, step=1)
    max_members = factory.Faker('pyint', min_value=10, max_value=10000, step=1)
    is_top = factory.Faker('boolean', chance_of_getting_true=50)
    is_hot = factory.Faker('boolean', chance_of_getting_true=50)
    status = factory.fuzzy.FuzzyChoice(Event.STATUS_TYPES, getter=lambda c: c[0])

    class Meta:
        exclude = ['organizer']
        abstract = True


class EventUserWithoutPlaceFactory(EventAbstractFactory):
    organizer = factory.SubFactory(UserFactory)
    address = factory.SubFactory(AddressFactory)

    class Meta:
        model = Event
        abstract = False


class EventUserWithPlaceFactory(EventAbstractFactory):
    organizer = factory.SubFactory(UserFactory)
    place = factory.SubFactory(PlaceFactory)
    address = factory.SelfAttribute('place.address')

    class Meta:
        model = Event
        abstract = False


class EventOrganizerWithoutPlaceFactory(EventAbstractFactory):
    organizer = factory.SubFactory(MemberListFactory)
    organizer_type = factory.LazyAttribute(
        lambda x: ContentType.objects.get_for_model(Organization)
    )
    address = factory.SubFactory(AddressFactory)

    class Meta:
        model = Event
        abstract = False


class EventOrganizerWithPlaceFactory(EventAbstractFactory):
    organizer = factory.SubFactory(MemberListFactory)
    organizer_type = factory.LazyAttribute(
        lambda x: ContentType.objects.get_for_model(Organization)
    )

    place = factory.SubFactory(PlaceFactory)
    address = factory.SelfAttribute('place.address')

    class Meta:
        model = Event
        abstract = False
