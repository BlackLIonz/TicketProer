import pytest
from pytest_factoryboy import register
from rest_auth.app_settings import create_token, TokenSerializer
from rest_auth.models import TokenModel

from apps.events.factories import EventOrganizerWithPlaceFactory, EventUserWithPlaceFactory
from apps.feedbacks.factories import (
    CommentToOrganizationFactory,
    CommentToEventFactory,
    CommentToPlaceFactory,
    CommentToReviewFactory,
)
from apps.feedbacks.factories import ReviewFactory
from apps.feedbacks.models import Comment
from apps.locations.factories import PlaceFactory, AddressFactory
from apps.users.factories import UserFactory, OrganizationFactory

register(UserFactory, 'user')
register(PlaceFactory, 'place')
register(OrganizationFactory, 'organization')
register(AddressFactory, 'address')
register(EventOrganizerWithPlaceFactory, 'event')
register(EventUserWithPlaceFactory, 'event2')
register(CommentToOrganizationFactory, 'comment_to_organization')
register(CommentToEventFactory, 'comment_to_event')
register(CommentToPlaceFactory, 'comment_to_place')
register(CommentToReviewFactory, 'comment_to_review')


@pytest.fixture
def token(user):
    return create_token(TokenModel, user, TokenSerializer)


@pytest.fixture
def review_dict():
    return {
        'rating': 5,
        'text': 'Hello world'
    }


@pytest.fixture
def review_qty():
    return 1


@pytest.fixture
def comment_qty():
    return 1


@pytest.fixture
def comment_dict():
    return {
        "parent": None,
        "topic": None,
        "text": "Just a comment",
    }


@pytest.fixture
def comments_batch(comment_qty):
    number = comment_qty // 3
    query = CommentToOrganizationFactory.create_batch(size=number, status=Comment.OK)
    query += CommentToPlaceFactory.create_batch(size=number, status=Comment.OK)
    query += CommentToEventFactory.create_batch(size=number, status=Comment.OK)
    return query


@pytest.fixture
def review(users, events, places, organizations):
    return ReviewFactory.create_batch(size=1)


@pytest.fixture
def reviews(review_qty, users, events, places, organizations):
    return ReviewFactory.create_batch(size=review_qty)


@pytest.fixture
def places():
    return PlaceFactory.create_batch(size=100)


@pytest.fixture
def events():
    return EventOrganizerWithPlaceFactory.create_batch(size=10)


@pytest.fixture
def organizations():
    return OrganizationFactory.create_batch(size=10)


@pytest.fixture
def users():
    return UserFactory.create_batch(size=10)

