from django.db import models

from tools.image_funcs import get_image_path
from apps.base.models.base import BaseAbstractModel
from apps.locations.models.address import Address


class Place(BaseAbstractModel):
    WORKING = 'WORKING'
    TEMPORARILY_CLOSED = 'TEMPORARILY_CLOSED'
    CLOSED = 'CLOSED'
    STATUS_CHOICES = [
        (TEMPORARILY_CLOSED, 'Temporarily closed'),
        (WORKING, 'Working'),
        (CLOSED, 'Closed'),
    ]
    name = models.CharField(max_length=75, blank=False, null=False)
    address = models.OneToOneField(Address, on_delete=models.PROTECT)
    photo = models.ImageField(upload_to=get_image_path, blank=True, null=True)
    description = models.CharField(max_length=200, blank=True, null=True)
    status = models.CharField(max_length=18, choices=STATUS_CHOICES, blank=False, null=False)
