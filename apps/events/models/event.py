from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from apps.base.models import BaseAbstractModel
from apps.locations.models import Place, Address

from tools.image_funcs import get_image_path


class Event(BaseAbstractModel):
    SOON = "SOON"
    SUCCEED = "SUCCEED"
    REJECTED = "REJECTED"
    STATUS_TYPES = (
        (SOON, "soon"),
        (SUCCEED, "succeed"),
        (REJECTED, "rejected"),
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

    def __str__(self):
        return self.name

    # TODO
    # @property
    # def rating(self):
    #     pass
