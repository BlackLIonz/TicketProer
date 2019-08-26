from tools.image_funcs import get_profile_image_path
from django.db import models
from apps.base.models import BaseAbstractModel


class Organization(BaseAbstractModel):
    name = models.CharField(max_length=150, blank=False, null=False)
    email = models.EmailField(blank=False, null=False)
    profile_image = models.ImageField(upload_to=get_profile_image_path, blank=True, null=True)
    description = models.TextField(blank=True, null=False)
    approved = models.BooleanField(default=False)
