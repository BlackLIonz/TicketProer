import datetime
import json

import pytest
from rest_framework import status

from apps.events.models import Event
from apps.subscriptions.models import Subscription


@pytest.mark.django_db
class TestUserSubscriptions:
    @pytest.mark.parametrize('subscription_qty', [0, 1, 10, 50])
    def test_user_subscriptions_for_staff_true(self, client, request_user, user, token, subscriptions, subscription_qty):
        request_user.is_staff = True
        request_user.save()
        for subscription in subscriptions:
            subscription.user = user
            subscription.save()
        res = client.get(f'/api/users/{user.id}/subscriptions/', **{'HTTP_AUTHORIZATION': f'Token {str(token)}'})
        assert res.status_code == status.HTTP_200_OK
        assert len(res.json()) == subscription_qty

    def test_user_subscriptions_for_staff_false(self, client, request_user, user, token):
        res = client.get(f'/api/users/{user.id}/subscriptions/', **{'HTTP_AUTHORIZATION': f'Token {str(token)}'})
        assert res.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestSubscriptions:
    @pytest.mark.parametrize('subscription_qty', [0, 1, 10, 50])
    def test_list_for_staff(self, client, request_user, token, subscriptions, subscription_qty):
        request_user.is_staff = True
        request_user.save()
        res = client.get(f'/api/subscriptions/', **{'HTTP_AUTHORIZATION': f'Token {str(token)}'})
        assert res.status_code == status.HTTP_200_OK
        assert len(res.json()) == subscription_qty

    @pytest.mark.parametrize('subscription_qty', [0, 1, 10, 50])
    def test_list_for_regular_user(self, client, request_user, token, subscriptions, subscription_qty):
        res = client.get(f'/api/subscriptions/', **{'HTTP_AUTHORIZATION': f'Token {str(token)}'})
        assert res.status_code == status.HTTP_403_FORBIDDEN

    def test_retrieve_for_staff(self, client, request_user, owner, token, subscription):
        request_user.is_staff = True
        request_user.save()
        subscription.user = owner
        subscription.status = Subscription.STATUS_ACTIVE
        subscription.save()
        res = client.get(f'/api/subscriptions/{subscription.id}/', **{'HTTP_AUTHORIZATION': f'Token {str(token)}'})
        sub = res.json()
        assert res.status_code == status.HTTP_200_OK
        assert sub.get('event') == str(subscription.event.id)
        assert sub.get('status') == subscription.status

    def test_retrieve_for_regular_user(self, client, request_user, owner, token, subscription):
        subscription.user = owner
        subscription.status = Subscription.STATUS_ACTIVE
        subscription.save()
        res = client.get(f'/api/subscriptions/{subscription.id}/', **{'HTTP_AUTHORIZATION': f'Token {str(token)}'})
        assert res.status_code == status.HTTP_403_FORBIDDEN

    def test_retrieve_for_owner(self, client, request_user, token, subscription, subscription_qty):
        subscription.user = request_user
        subscription.status = Subscription.STATUS_ACTIVE
        subscription.save()
        res = client.get(f'/api/subscriptions/{subscription.id}/', **{'HTTP_AUTHORIZATION': f'Token {str(token)}'})
        sub = res.json()
        assert res.status_code == status.HTTP_200_OK
        assert sub.get('user') == str(request_user.id)
        assert sub.get('event') == str(subscription.event.id)
        assert sub.get('status') == subscription.status

    def test_retrieve_for_deleted_subscription(self, client, request_user, token, subscription):
        subscription.user = request_user
        subscription.status = Subscription.STATUS_CANCELLED
        subscription.save()
        res = client.get(f'/api/subscriptions/{subscription.id}/', **{'HTTP_AUTHORIZATION': f'Token {str(token)}'})
        assert res.status_code == status.HTTP_404_NOT_FOUND

    def test_retrieve_detail_for_random_id(self, client, request_user, token, subscription):
        subscription.user = request_user
        subscription.status = Subscription.STATUS_CANCELLED
        subscription.save()
        res = client.get(f'/api/subscriptions/ghjklasfg/', **{'HTTP_AUTHORIZATION': f'Token {str(token)}'})
        assert res.status_code == status.HTTP_404_NOT_FOUND

    def test_destroy_for_staff(self, client, request_user, owner, token, subscription):
        request_user.is_staff = True
        request_user.save()
        subscription.user = owner
        subscription.status = Subscription.STATUS_ACTIVE
        subscription.save()
        res = client.delete(f'/api/subscriptions/{subscription.id}/', **{'HTTP_AUTHORIZATION': f'Token {str(token)}'})
        assert res.status_code == status.HTTP_403_FORBIDDEN

    def test_destroy_for_regular_user(self, client, request_user, owner, token, subscription):
        subscription.user = owner
        subscription.status = Subscription.STATUS_ACTIVE
        subscription.save()
        res = client.delete(f'/api/subscriptions/{subscription.id}/', **{'HTTP_AUTHORIZATION': f'Token {str(token)}'})
        assert res.status_code == status.HTTP_403_FORBIDDEN

    def test_destroy_for_owner(self, client, request_user, token, subscription, subscription_qty):
        subscription.user = request_user
        subscription.status = Subscription.STATUS_ACTIVE
        subscription.save()
        res = client.delete(f'/api/subscriptions/{subscription.id}/', **{'HTTP_AUTHORIZATION': f'Token {str(token)}'})
        subscription.refresh_from_db()
        assert res.status_code == status.HTTP_204_NO_CONTENT
        assert subscription.status == Subscription.STATUS_CANCELLED

    def test_destroy_for_deleted_subscription(self, client, request_user, token, subscription):
        subscription.user = request_user
        subscription.status = Subscription.STATUS_CANCELLED
        subscription.save()
        res = client.delete(f'/api/subscriptions/{subscription.id}/', **{'HTTP_AUTHORIZATION': f'Token {str(token)}'})
        assert res.status_code == status.HTTP_404_NOT_FOUND

    def test_destroy_detail_for_random_id(self, client, request_user, token, subscription):
        subscription.user = request_user
        subscription.status = Subscription.STATUS_CANCELLED
        subscription.save()
        res = client.delete(f'/api/subscriptions/ghjklasfg/', **{'HTTP_AUTHORIZATION': f'Token {str(token)}'})
        assert res.status_code == status.HTTP_404_NOT_FOUND

    def test_partial_update_for_staff(self, client, request_user, token, subscription):
        request_user.is_staff = True
        request_user.save()
        subscription.status = Subscription.STATUS_ACTIVE
        subscription.save()
        new_data = {'status': 'REJECTED'}
        res = client.patch(f'/api/subscriptions/{subscription.id}/',
                           data=json.dumps(new_data),
                           content_type='application/json',
                           **{'HTTP_AUTHORIZATION': f'Token {str(token)}'})
        assert res.status_code == status.HTTP_200_OK
        data = res.json()
        assert data.get('status') == new_data.get('status')

    def test_partial_update_for_regular_user(self, client, request_user, token, subscription):
        subscription.status = Subscription.STATUS_ACTIVE
        subscription.save()
        new_data = {'status': 'REJECTED'}
        res = client.patch(f'/api/subscriptions/{subscription.id}/',
                           data=json.dumps(new_data),
                           content_type='application/json',
                           **{'HTTP_AUTHORIZATION': f'Token {str(token)}'})
        assert res.status_code == status.HTTP_403_FORBIDDEN

    def test_create_ok(self, client, request_user, event, token):
        sub = {'event': f'{str(event.id)}'}
        event.status = Event.SOON
        event.date += datetime.timedelta(50)
        event.save()
        res = client.post(f'/api/subscriptions/',
                          data=json.dumps(sub),
                          content_type='application/json',
                          **{'HTTP_AUTHORIZATION': f'Token {str(token)}'})
        assert res.status_code == status.HTTP_201_CREATED
        data = res.json()
        assert data.get('user') == str(request_user.id)
        assert data.get('event') == str(event.id)
        assert data.get('status') == Subscription.STATUS_UNTRACKED

    def test_create_not_authenticated(self, client, event):
        sub = {'event': f'{str(event.id)}'}
        res = client.post(f'/api/subscriptions/', data=json.dumps(sub), content_type='application/json')
        assert res.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_without_event_id(self, client, request_user, token):
        sub = {}
        res = client.post(f'/api/subscriptions/',
                          data=json.dumps(sub),
                          content_type='application/json',
                          **{'HTTP_AUTHORIZATION': f'Token {str(token)}'})
        assert res.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_with_empty_event_id(self, client, request_user, token):
        sub = {'event': ''}
        res = client.post(f'/api/subscriptions/',
                          data=json.dumps(sub),
                          content_type='application/json',
                          **{'HTTP_AUTHORIZATION': f'Token {str(token)}'})
        assert res.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_with_bad_event_id(self, client, request_user, token):
        sub = {'event': 'jhggkjh'}
        res = client.post(f'/api/subscriptions/',
                          data=json.dumps(sub),
                          content_type='application/json',
                          **{'HTTP_AUTHORIZATION': f'Token {str(token)}'})
        assert res.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_with_wrong_event_id(self, client, request_user, token):
        sub = {'event': 'cee51c29-1c13-493e-bbdd-f2fbf931dd35'}
        res = client.post(f'/api/subscriptions/',
                          data=json.dumps(sub),
                          content_type='application/json',
                          **{'HTTP_AUTHORIZATION': f'Token {str(token)}'})
        assert res.status_code == status.HTTP_404_NOT_FOUND

    def test_create_with_unsubscribabale_event(self, client, request_user, event, token):
        sub = {'event': f'{str(event.id)}'}
        event.status = Event.SUCCEED
        event.date -= datetime.timedelta(50)
        event.save()
        res = client.post(f'/api/subscriptions/',
                          data=json.dumps(sub),
                          content_type='application/json',
                          **{'HTTP_AUTHORIZATION': f'Token {str(token)}'})
        assert res.status_code == status.HTTP_403_FORBIDDEN

    def test_create_with_existing_subscription(self, client, request_user, event, token, subscription):
        sub = {'event': f'{str(event.id)}'}
        event.status = Event.SOON
        event.date += datetime.timedelta(50)
        event.save()
        subscription.user = request_user
        subscription.event = event
        subscription.status = Subscription.STATUS_ACTIVE
        subscription.save()
        res = client.post(f'/api/subscriptions/',
                          data=json.dumps(sub),
                          content_type='application/json',
                          **{'HTTP_AUTHORIZATION': f'Token {str(token)}'})
        assert res.status_code == status.HTTP_409_CONFLICT

    def test_create_with_deleted_subscription(self, client, request_user, event, token, subscription):
        sub = {'event': f'{str(event.id)}'}
        event.status = Event.SOON
        event.date += datetime.timedelta(50)
        event.save()
        subscription.user = request_user
        subscription.event = event
        subscription.status = Subscription.STATUS_CANCELLED
        subscription.save()
        res = client.post(f'/api/subscriptions/',
                          data=json.dumps(sub),
                          content_type='application/json',
                          **{'HTTP_AUTHORIZATION': f'Token {str(token)}'})
        assert res.status_code == status.HTTP_201_CREATED
        data = res.json()
        assert data.get('user') == str(request_user.id)
        assert data.get('event') == str(event.id)
        assert data.get('status') == Subscription.STATUS_UNTRACKED

    def test_approve_ok(self, client, request_user, token, subscription, event):
        event.status = Event.SOON
        event.date += datetime.timedelta(50)
        event.save()
        subscription.user = request_user
        subscription.event = event
        subscription.STATUS_UNTRACKED
        subscription.save()
        res = client.post(f'/api/subscriptions/{subscription.id}/approve/',
                          **{'HTTP_AUTHORIZATION': f'Token {str(token)}'})
        assert res.status_code == status.HTTP_200_OK
