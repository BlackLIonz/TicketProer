from apps.base.models.UUID import UUIDAbstractModel
from apps.base.models.timestamp import TimestampAbstractModel


class BaseAbstractModel(TimestampAbstractModel, UUIDAbstractModel):
    class Meta:
        abstract = True
