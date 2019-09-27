from django.contrib.contenttypes.fields import GenericRelation
from django.db import models

from apps.base.models import BaseAbstractModel, ParentTopicRelationModel
from tools.image_funcs import get_image_path


class Organization(BaseAbstractModel, ParentTopicRelationModel):
    name = models.CharField(max_length=150, blank=False, null=False)
    email = models.EmailField(blank=False, null=False)
    profile_image = models.ImageField(upload_to=get_image_path, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    approved = models.BooleanField(default=False)
    events = GenericRelation(
        'events.Event',
        content_type_field='organizer_type',
        object_id_field='organizer_id',
        related_name='events'
    )
    reviews = GenericRelation(
        'feedbacks.Review',
        content_type_field='parent_object_type',
        object_id_field='parent_object_id',
    )

    class Meta:
        ordering = ['name']

    @property
    def all_events(self):
        return self.events.all()

    @property
    def all_members(self):
        return [i.member for i in self.membership.all()]

    def __str__(self):
        return self.name
