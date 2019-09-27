from django.db import models

from apps.base.models import BaseAbstractModel


class Subscription(BaseAbstractModel):
    STATUS_ACTIVE = 'ACTIVE'
    STATUS_REJECTED = 'REJECTED'
    STATUS_UNPAID = 'UNPAID'
    STATUS_UNTRACKED = 'UNTRACKED'
    STATUS_CANCELLED = 'CANCELLED'
    STATUS_CHOICES = [
        (STATUS_ACTIVE, 'Active'),
        (STATUS_REJECTED, 'Rejected'),
        (STATUS_UNPAID, 'Unpaid'),
        (STATUS_UNTRACKED, 'Untracked'),
        (STATUS_CANCELLED, 'Cancelled'),
    ]
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='subscriptions')
    event = models.ForeignKey('events.Event', on_delete=models.CASCADE, related_name='subscribers')
    status = models.CharField(max_length=9, choices=STATUS_CHOICES, blank=False, null=False, default=STATUS_UNTRACKED)

    class Meta:
        unique_together = ['user', 'event']

    def set_status(self, status):
        self.status = status
        self.save()

    def __str__(self):
        return f'{self.event.name}: {self.user.email}'
