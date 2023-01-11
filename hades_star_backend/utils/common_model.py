import uuid
from typing import Any

from dirtyfields import DirtyFieldsMixin
from django.db import models
from django.db.models import QuerySet
from django.utils.timezone import now


class CommonManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(deleted_at__isnull=True)

    def with_deleted(self) -> QuerySet:
        return super().get_queryset()


class CommonModel(DirtyFieldsMixin, models.Model):

    id = models.UUIDField(
        primary_key=True, unique=True, null=False, editable=False, default=uuid.uuid4
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = CommonManager()

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.previous_changes = {}
        super().__init__(*args, **kwargs)

    def __strip_whitespace_from_charfields(self) -> None:
        for field in self._meta.fields:
            field_name = getattr(self, field.name)

            if isinstance(field, models.CharField) and field_name:
                setattr(self, field.name, str(field_name).strip())

    @property
    def is_being_created(self) -> bool:
        return True if self._state.adding else False

    @property
    def changes(self):
        return self.get_dirty_fields(check_relationship=True)

    def save(self, *args, **kwargs):
        self.previous_changes = self.changes
        self.__strip_whitespace_from_charfields()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.deleted_at = now()
        self.save()

    def delete_forever(self, *args, **kwargs):
        super().delete(*args, **kwargs)

    class Meta:
        abstract = True
