import json
import random

import pytest
from rest_framework import status

from apps.feedbacks.models import Review


@pytest.mark.django_db
class TestReview:
    def test_create_with_event(self, client, review_dict, user, token, event):
        review_dict['parent_object'] = str(event.id)
        res = client.post('/api/reviews/',
                          data=json.dumps(review_dict),
                          content_type='application/json',
                          **{'HTTP_AUTHORIZATION': f'Token {token}'})
        assert res.status_code == status.HTTP_201_CREATED
        res_dict = res.json()
        assert res_dict.get('parent_object_id') == review_dict['parent_object']
        assert res_dict.get('rating') == review_dict['rating']
        assert res_dict.get('text') == review_dict['text']

    def test_create_with_organization(self, client, review_dict, token, organization):
        review_dict['parent_object'] = str(organization.id)
        res = client.post('/api/reviews/',
                          data=json.dumps(review_dict),
                          content_type='application/json',
                          **{'HTTP_AUTHORIZATION': f'Token {token}'})
        assert res.status_code == status.HTTP_201_CREATED
        res_dict = res.json()
        assert res_dict.get('parent_object_id') == review_dict['parent_object']
        assert res_dict.get('rating') == review_dict['rating']
        assert res_dict.get('text') == review_dict['text']

    def test_create_with_place(self, client, review_dict, token, place):
        review_dict['parent_object'] = str(place.id)
        res = client.post('/api/reviews/',
                          data=json.dumps(review_dict),
                          content_type='application/json',
                          **{'HTTP_AUTHORIZATION': f'Token {token}'})
        assert res.status_code == status.HTTP_201_CREATED
        res_dict = res.json()
        assert res_dict.get('parent_object_id') == review_dict['parent_object']
        assert res_dict.get('rating') == review_dict['rating']
        assert res_dict.get('text') == review_dict['text']

    @pytest.mark.parametrize('review_qty', [10])
    def test_retrieve(self, client, reviews, review_qty):
        random_review = random.choice(Review.objects.filter(status__in=[Review.OK, Review.SUSPICIOUS]))
        res = client.get(f'/api/reviews/{random_review.id}/')
        assert res.status_code == status.HTTP_200_OK
        res_dict = res.json()
        assert res_dict.get('id') == str(random_review.id)
        assert res_dict.get('text') == random_review.text
        assert res_dict.get('rating') == random_review.rating

    @pytest.mark.parametrize('review_qty', [20])
    def test_destroy(self, client, reviews, user, review_qty, token):
        user.is_staff = True
        user.save()
        random_review = random.choice(reviews)
        res = client.delete(f'/api/reviews/{random_review.id}/', **{'HTTP_AUTHORIZATION': f'Token {user.auth_token}'})
        assert res.status_code == status.HTTP_204_NO_CONTENT
        assert not Review.objects.filter(status__in=[Review.OK, Review.SUSPICIOUS], id=random_review.id).exists()

    @pytest.mark.parametrize('review_qty', [10])
    def test_list(self, client, reviews, review_qty):
        res = client.get(f'/api/reviews/')
        assert res.status_code == status.HTTP_200_OK
        res_dict = res.json()
        assert len(res_dict) != len(reviews)

    def test_partial_update(self, client, user, token, reviews, review_dict):
        user.is_staff = True
        user.save()
        random_review = random.choice(reviews)
        random_review.status = Review.OK
        random_review.save()
        res = client.put(f'/api/reviews/{random_review.id}/',
                         data=json.dumps(review_dict),
                         content_type='application/json',
                         **{'HTTP_AUTHORIZATION': f'Token {token}'})
        assert res.status_code == status.HTTP_200_OK
        res_dict = res.json()
        assert res_dict.get('text') == review_dict['text']
        assert res_dict.get('rating') == review_dict['rating']
