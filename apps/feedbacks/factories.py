import random

import factory.fuzzy
from django.contrib.contenttypes.models import ContentType
from faker import Factory as FakeFactory

from apps.events.models import Event
from apps.feedbacks.models import Review
from apps.locations.models import Place
from apps.users.factories import UserFactory
from apps.users.models import User, Organization

faker = FakeFactory.create()


class ReviewFactory(factory.django.DjangoModelFactory):
    rating = factory.LazyAttribute(lambda x: random.randint(1, 10))
    text = factory.Faker('text', max_nb_chars=200, ext_word_list=None)
    parent_object_id = factory.SelfAttribute('parent_object.id')
    parent_object_type = factory.LazyAttribute(
        lambda o: ContentType.objects.get_for_model(o.parent_object)
    )
    parent_object = factory.LazyAttribute(
        lambda x: random.choice(
            list(Organization.objects.all()) + list(Event.objects.all()) + list(Place.objects.all())
        )
    )
    created_by = factory.SubFactory(UserFactory)
    status = factory.fuzzy.FuzzyChoice(Review.STATUS_TYPES, getter=lambda c: c[0])

    class Meta:
        model = Review
        abstract = False
