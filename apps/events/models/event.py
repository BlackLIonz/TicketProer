from datetime import datetime, timedelta


import pytz


from django.core import validators
from django.db import models
from django.db.models import signals
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.dispatch import receiver


from apps.base.models import BaseAbstractModel, ParentTopicRelationModel
from apps.locations.models import Place, Address
from tools.image_funcs import get_image_path
from apps.subscriptions.tasks import delete_subscriptions


class Event(BaseAbstractModel, ParentTopicRelationModel):
    SOON = 'SOON'
    SUCCEED = 'SUCCEED'
    REJECTED = 'REJECTED'
    STATUS_TYPES = (
        (SOON, 'soon'),
        (SUCCEED, 'succeed'),
        (REJECTED, 'rejected'),
    )

    name = models.CharField(max_length=64, blank=False, null=False)
    description = models.TextField(blank=False, null=False)
    poster = models.ImageField(upload_to=get_image_path, blank=True, null=True)
    organizer_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    organizer_id = models.UUIDField()
    organizer = GenericForeignKey('organizer_type', 'organizer_id')
    place = models.ForeignKey(Place, on_delete=models.CASCADE, blank=True, null=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, blank=False, null=False)
    date = models.DateTimeField(blank=False, null=False)
    duration = models.DurationField(blank=False, null=False)
    age_rate = models.PositiveSmallIntegerField(default=18, blank=False, null=False)
    is_approved = models.BooleanField(default=False)
    is_hot = models.BooleanField(default=False)
    is_top = models.BooleanField(default=False)
    max_members = models.PositiveIntegerField(blank=False, null=False)
    status = models.CharField(max_length=16, choices=STATUS_TYPES, default=SOON)
    rating = models.PositiveSmallIntegerField(default=0, blank=False, null=False, validators=[
        validators.MaxValueValidator(10),
        validators.MinValueValidator(1)
    ])
    reviews = GenericRelation(
        'feedbacks.Review',
        content_type_field='parent_object_type',
        object_id_field='parent_object_id',
    )

    def __str__(self):
        return self.name

    @property
    def registered_users(self):
        return self.subscribers.all().count()

    @property
    def is_available_for_feedback(self):
        return True if self.date <= datetime.utcnow().replace(tzinfo=pytz.utc) else False

    @property
    def is_available_for_subscription(self):
        return True if datetime.utcnow().replace(tzinfo=pytz.utc) <= self.date - timedelta(hours=1) else False


@receiver(signals.pre_save, sender=Event)
def on_status_active_save(sender, instance, **kwargs):
    old_instance = Event.objects.get(id=instance.id)
    if instance.is_approved and not old_instance.is_approved:
        delete_subscriptions.apply_async(args=[instance.id], eta=instance.date - timedelta(hours=1))
