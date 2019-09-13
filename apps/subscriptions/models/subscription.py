from django.db import models

from apps.base.models import BaseAbstractModel
from apps.events.models import Event
from apps.users.models import User


class Subscription(BaseAbstractModel):
    STATUS_ACTIVE = 'ACTIVE'
    STATUS_REJECTED = 'REJECTED'
    STATUS_UNPAID = 'UNPAID'
    STATUS_UNTRACKED = 'UNTRACKED'
    STATUS_CHOICES = [
        (STATUS_ACTIVE, 'Active'),
        (STATUS_REJECTED, 'Rejected'),
        (STATUS_UNPAID, 'Unpaid'),
        (STATUS_UNTRACKED, 'Untracked')
    ]
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events')
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='subscribers')
    status = models.CharField(max_length=9, choices=STATUS_CHOICES, blank=False, null=False, default=STATUS_UNTRACKED)

    class Meta:
        unique_together = ['user_id', 'event_id']
