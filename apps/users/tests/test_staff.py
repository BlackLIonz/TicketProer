from datetime import datetime

import pytest
import iso8601
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestStaff:
    """Test user details for staff

    * check for valid data
    * check for staff/usual users
    """
    def test_user_details_for_staff_true(self, client, request_user, user, token):
        request_user.is_staff = True
        request_user.save()
        response = client.get(f'/api/user/{user.id}/', **{'HTTP_AUTHORIZATION': f'Token {str(token)}'})
        response_dict = response.json()
        assert response.status_code == HTTP_200_OK
        assert response_dict.get('username') == user.username
        assert response_dict.get('email') == user.email
        assert response_dict.get('id') == str(user.id)
        assert iso8601.parse_date(response_dict.get('created')) == user.created
        assert iso8601.parse_date(response_dict.get('updated')) == user.updated
        assert response_dict.get('first_name') == user.first_name
        assert response_dict.get('last_name') == user.last_name
        assert datetime.strptime(response_dict.get('date_of_birth'), '%Y-%m-%d').date() == user.date_of_birth
        assert 'password' not in response_dict
        assert response_dict.get('is_staff') == user.is_staff
        assert response_dict.get('is_active') == user.is_active
        assert response_dict.get('profile_image') == user.profile_image

    def test_user_details_for_staff_false(self, client, request_user, user, token):
        response = client.get(f'/api/user/{user.id}/', **{'HTTP_AUTHORIZATION': f'Token {str(token)}'})
        assert response.status_code == HTTP_403_FORBIDDEN
