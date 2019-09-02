from django.db import models
from apps.base.models import BaseAbstractModel
from apps.users.models import Organization, User


class MembersList(BaseAbstractModel):
    member = models.OneToOneField(User, related_name='membership', unique=True, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, blank=False, null=False, on_delete=models.CASCADE)
