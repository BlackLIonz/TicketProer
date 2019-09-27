import json

import pytest
from rest_framework import status

from apps.events.models import Event
from apps.feedbacks.models import Comment, Review
from apps.locations.models import Place
from apps.users.models import Organization


@pytest.mark.django_db
class TestComment:
    def test_negative_create_comment_unauthenticated_user(self, client, comment_dict, user, event2):
        user.save()
        event2.save()
        myevent = Event.objects.all()[0]
        comment_dict.update(parent={'id': str(myevent.id)})
        comment_dict.update(parent_type=myevent.__class__.__name__)
        comment_dict.update(topic={'id': str(myevent.id)})
        comment_dict.update(topic_type=myevent.__class__.__name__)
        res = client.post('/api/comments/', data=json.dumps(comment_dict),
                          content_type='application/json')
        assert res.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_comment_to_event(self, client, comment_dict, user, token, event2):
        user.save()
        event2.save()
        myobj = Event.objects.all()[0]
        comment_dict.update(parent={'id': str(myobj.id)})
        comment_dict.update(parent_type=myobj.__class__.__name__)
        comment_dict.update(topic={'id': str(myobj.id)})
        comment_dict.update(topic_type=myobj.__class__.__name__)
        res = client.post('/api/comments/', data=json.dumps(comment_dict),
                          content_type='application/json',
                          **{'HTTP_AUTHORIZATION': 'Token ' + str(token)})
        assert res.status_code == status.HTTP_201_CREATED
        res_obj = res.json()
        assert res_obj.get('id')
        db_comment = Comment.objects.get(id=res_obj.get('id'))
        assert db_comment.text == res_obj.get('text')

    def test_create_comment_to_organization(self, client, comment_dict, user, token, organization):
        user.save()
        organization.save()
        myobj = Organization.objects.all()[0]
        comment_dict.update(parent={'id': str(myobj.id)})
        comment_dict.update(parent_type=myobj.__class__.__name__)
        comment_dict.update(topic={'id': str(myobj.id)})
        comment_dict.update(topic_type=myobj.__class__.__name__)
        res = client.post('/api/comments/', data=json.dumps(comment_dict),
                          content_type='application/json',
                          **{'HTTP_AUTHORIZATION': 'Token ' + str(token)})
        assert res.status_code == status.HTTP_201_CREATED
        res_obj = res.json()
        assert res_obj.get('id')
        db_comment = Comment.objects.get(id=res_obj.get('id'))
        assert db_comment.text == res_obj.get('text')

    def test_create_comment_to_place(self, client, comment_dict, user, token, place):
        user.save()
        place.save()
        myobj = Place.objects.all()[0]
        comment_dict.update(parent={'id': str(myobj.id)})
        comment_dict.update(parent_type=myobj.__class__.__name__)
        comment_dict.update(topic={'id': str(myobj.id)})
        comment_dict.update(topic_type=myobj.__class__.__name__)
        res = client.post('/api/comments/', data=json.dumps(comment_dict),
                          content_type='application/json',
                          **{'HTTP_AUTHORIZATION': 'Token ' + str(token)})
        assert res.status_code == status.HTTP_201_CREATED
        res_obj = res.json()
        assert res_obj.get('id')
        db_comment = Comment.objects.get(id=res_obj.get('id'))
        assert db_comment.text == res_obj.get('text')

    def test_create_comment_to_review(self, client, comment_dict, user, token, review):
        user.save()
        myobj = Review.objects.all()[0]
        comment_dict.update(parent={'id': str(myobj.id)})
        comment_dict.update(parent_type=myobj.__class__.__name__)
        comment_dict.update(topic={'id': str(myobj.id)})
        comment_dict.update(topic_type=myobj.__class__.__name__)
        res = client.post('/api/comments/', data=json.dumps(comment_dict),
                          content_type='application/json',
                          **{'HTTP_AUTHORIZATION': 'Token ' + str(token)})
        assert res.status_code == status.HTTP_201_CREATED
        res_obj = res.json()
        assert res_obj.get('id')
        db_comment = Comment.objects.get(id=res_obj.get('id'))
        assert db_comment.text == res_obj.get('text')

    def test_create_comment_to_comment(self, client, comment_dict, user, token, organization):
        user.save()
        organization.save()
        myobj = Organization.objects.all()[0]
        comment_dict.update(parent={'id': str(myobj.id)})
        comment_dict.update(parent_type=myobj.__class__.__name__)
        comment_dict.update(topic={'id': str(myobj.id)})
        comment_dict.update(topic_type=myobj.__class__.__name__)
        client.post('/api/comments/', data=json.dumps(comment_dict),
                    content_type='application/json',
                    **{'HTTP_AUTHORIZATION': 'Token ' + str(token)})
        myobj_2 = Comment.objects.all()[0]
        comment_dict.update(parent={'id': str(myobj_2.id)})
        comment_dict.update(parent_type=myobj_2.__class__.__name__)
        comment_dict.update(topic={'id': str(myobj.id)})
        comment_dict.update(topic_type=myobj.__class__.__name__)
        res = client.post('/api/comments/', data=json.dumps(comment_dict),
                          content_type='application/json',
                          **{'HTTP_AUTHORIZATION': 'Token ' + str(token)})
        assert res.status_code == status.HTTP_201_CREATED
        res_obj = res.json()
        assert res_obj.get('id')
        db_comment = Comment.objects.get(id=res_obj.get('id'))
        assert db_comment.text == res_obj.get('text')

    @pytest.mark.parametrize('comment_qty', [0, 6, 12, 24])
    def test_list_comment(self, client, comments_batch, comment_qty):
        res = client.get(f'/api/comments/')
        assert res.status_code == status.HTTP_200_OK
        assert isinstance(res.json(), list)
        assert len(res.json()) == comment_qty

    def test_retrieve_comment(self, client, comment_to_place):
        db_comment = Comment.objects.first()
        res = client.get(f'/api/comments/{db_comment.id}/', content_type='application/json')
        assert res.status_code == status.HTTP_200_OK
        res_obj = res.json()
        assert str(db_comment.id) == res_obj.get('id')
        assert db_comment.text == res_obj.get('text')

    def test_update_comment(self, client, user, token, comment_dict, comment_to_organization):
        user.is_staff = True
        user.save()
        comment = Comment.objects.first()
        res = client.put(f'/api/comments/{comment.id}/', data=json.dumps(comment_dict),
                         content_type='application/json',
                         **{'HTTP_AUTHORIZATION': 'Token ' + str(token)})
        assert res.status_code == status.HTTP_200_OK
        res_dict = res.json()
        assert res_dict.get('text') == comment_dict.get('text')

    def test_partial_update_comment(self, client, user, token, comment_dict, comment_to_place):
        user.is_staff = True
        user.save()
        comment = Comment.objects.first()
        res = client.patch(f'/api/comments/{comment.id}/', data=json.dumps(comment_dict),
                           content_type='application/json',
                           **{'HTTP_AUTHORIZATION': 'Token ' + str(token)})
        assert res.status_code == status.HTTP_200_OK
        res_dict = res.json()
        assert res_dict.get('text') == comment_dict.get('text')

    @pytest.mark.parametrize('comment_qty', [6, 12, 24])
    def test_destroy(self, client, user, token, comments_batch, comment_qty):
        user.is_staff = True
        user.save()
        comment = Comment.objects.first()
        res = client.delete(f'/api/comments/{comment.id}/',
                            content_type='application/json',
                            **{'HTTP_AUTHORIZATION': 'Token ' + str(token)})
        assert res.status_code == status.HTTP_204_NO_CONTENT
        comment.refresh_from_db()
        res = client.delete(f'/api/comments/',
                            content_type='application/json',
                            **{'HTTP_AUTHORIZATION': 'Token ' + str(token)})
        res_dict = res.json()
        assert comment_qty - len(res_dict) == comment_qty - 1
        assert Comment.objects.get(id=comment.id) == comment
        assert comment.status == Comment.DELETED
