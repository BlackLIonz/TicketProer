import pytest
from rest_framework import status


@pytest.mark.django_db
class TestStaff:
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
        response = client.get(f'/api/users/{user.id}/subscriptions/', **{'HTTP_AUTHORIZATION': f'Token {str(token)}'})
        assert response.status_code == status.HTTP_403_FORBIDDEN
