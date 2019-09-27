import random

import factory.fuzzy
from django.contrib.contenttypes.models import ContentType
from faker import Factory as FakeFactory

from apps.events.factories import EventUserWithPlaceFactory
from apps.events.models import Event
from apps.feedbacks.models import Comment
from apps.feedbacks.models import Review
from apps.locations.factories import PlaceFactory
from apps.locations.models import Place
from apps.users.factories import UserFactory, OrganizationFactory
from apps.users.models import Organization

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


class CommentAbstractFactory(factory.django.DjangoModelFactory):
    text = factory.Faker('text', max_nb_chars=200, ext_word_list=None)
    topic_id = factory.SelfAttribute('topic.id')
    topic_type = factory.LazyAttribute(
        lambda o: ContentType.objects.get_for_model(o.topic)
    )
    parent_id = factory.SelfAttribute('parent.id')
    parent_type = factory.LazyAttribute(
        lambda o: ContentType.objects.get_for_model(o.parent)
    )
    status = factory.fuzzy.FuzzyChoice(Comment.OK)
    created_by = factory.SubFactory(UserFactory)

    class Meta:
        exclude = ['topic', 'parent']
        abstract = True


class CommentToOrganizationFactory(CommentAbstractFactory):
    topic = factory.SubFactory(OrganizationFactory)
    parent = factory.LazyAttribute(lambda o: o.topic)

    class Meta:
        model = Comment


class CommentToPlaceFactory(CommentAbstractFactory):
    topic = factory.SubFactory(PlaceFactory)
    parent = factory.LazyAttribute(lambda o: o.topic)

    class Meta:
        model = Comment


class CommentToEventFactory(CommentAbstractFactory):
    topic = factory.SubFactory(EventUserWithPlaceFactory)
    parent = factory.LazyAttribute(lambda o: o.topic)

    class Meta:
        model = Comment


class CommentToReviewFactory(CommentAbstractFactory):
    topic = factory.SubFactory(ReviewFactory)
    parent = factory.LazyAttribute(lambda o: o.topic)

    class Meta:
        model = Comment