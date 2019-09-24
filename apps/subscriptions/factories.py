import factory
import factory.fuzzy
from faker import Factory as FakeFactory

from apps.users.models import User
from apps.events.models import Event
from apps.subscriptions.models import Subscription
from apps.events.factories import EventUserWithoutPlaceFactory
from apps.users.factories import UserFactory


faker = FakeFactory.create()


class SubscriptionFactory(factory.django.DjangoModelFactory):
    user = factory.Iterator(User.objects.all())
    event = factory.Iterator(Event.objects.all())
    status = factory.fuzzy.FuzzyChoice(Subscription.STATUS_CHOICES, getter=lambda c: c[0])

    class Meta:
        model = Subscription


class SubscriptionFactoryForTests(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    event = factory.SubFactory(EventUserWithoutPlaceFactory)
    status = factory.fuzzy.FuzzyChoice(Subscription.STATUS_CHOICES, getter=lambda c: c[0])

    class Meta:
        model = Subscription
