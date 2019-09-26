from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models

from apps.base.models import BaseAbstractModel
from apps.subscriptions.models import Subscription
from tools.image_funcs import get_image_path


class User(AbstractUser, BaseAbstractModel):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    profile_image = models.ImageField(upload_to=get_image_path, blank=True, null=True)
    email = models.EmailField('email address', blank=False, null=False, unique=True)
    first_name = models.CharField('first name', max_length=30, blank=True, null=True)
    last_name = models.CharField('last name', max_length=150, blank=True, null=True)
    date_of_birth = models.DateField('date of birth', blank=True, null=True)
    events = GenericRelation(
        'events.Event',
        content_type_field='organizer_type',
        object_id_field='organizer_id',
        related_name='events'
    )

    @property
    def all_active_subscriptions(self):
        return self.subscriptions.exclude(status=Subscription.STATUS_CANCELLED)
