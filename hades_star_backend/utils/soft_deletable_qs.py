from django.core.exceptions import FieldDoesNotExist
from django.db import models
from django.utils import timezone


class SoftDeletableQS(models.QuerySet):
    """Queryset allows soft-deltete on its objects"""

    def delete(self, **kwargs):
        """Softly delete object"""
        try:
            self.update(is_active=False, deleted_at=timezone.now(), **kwargs)
        except FieldDoesNotExist:
            self.update(status="inactive", deleted_at=timezone.now(), **kwargs)

    def hard_delete(self, **kwargs):
        """Remove object from database permanently"""
        super().delete(**kwargs)
