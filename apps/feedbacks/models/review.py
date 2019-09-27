from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core import validators
from django.db import models

from apps.base.models import BaseAbstractModel, ParentTopicRelationModel
from apps.users.models import User


class Review(BaseAbstractModel, ParentTopicRelationModel):
    OK = 'OK'
    SUSPICIOUS = 'SUSPICIOUS'
    DELETED = 'DELETED'
    CANCELED = 'CANCELED'
    STATUS_TYPES = (
        (OK, 'ok'),
        (SUSPICIOUS, 'suspicious'),
        (DELETED, 'deleted'),
        (CANCELED, 'canceled'),
    )

    rating = models.PositiveSmallIntegerField(blank=False, null=False, validators=[
        validators.MaxValueValidator(10),
        validators.MinValueValidator(1)
    ])
    text = models.TextField(null=False, blank=False)
    created_by = models.ForeignKey(User, editable=False, null=False, blank=False,
                                   on_delete=models.CASCADE, related_name='reviews')
    parent_object_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    parent_object = GenericForeignKey('parent_object_type', 'parent_object_id')
    parent_object_id = models.UUIDField(editable=False)
    status = models.CharField(max_length=16, choices=STATUS_TYPES, default=OK)

    class Meta:
        unique_together = ['parent_object_id', 'created_by']

    def __str__(self):
        return f'Review from {self.created_by.username} on {self.parent_object.name}'
