from django.db import models
from django.utils import timezone


class SoftDeleteQuerySet(models.QuerySet):
    """QuerySet that supports soft deletion."""

    def delete(self):
        """Soft delete multiple records."""
        return self.update(is_deleted=True, deleted_at=timezone.now())

    def hard_delete(self):
        """Permanently delete records."""
        return super().delete()

    def alive(self):
        """Filter records that are not deleted."""
        return self.filter(is_deleted=False)

    def dead(self):
        """Filter records that are deleted."""
        return self.filter(is_deleted=True)


class SoftDeleteManager(models.Manager):
    """Manager that supports soft deletion."""

    def __init__(self, *args, **kwargs):
        self.alive_only = kwargs.pop("alive_only", True)
        super().__init__(*args, **kwargs)

    def get_queryset(self):
        if self.alive_only:
            return SoftDeleteQuerySet(self.model).filter(is_deleted=False)
        return SoftDeleteQuerySet(self.model)

    def hard_delete(self):
        return self.get_queryset().hard_delete()


class RemediumBaseModel(models.Model):
    """
    Base model for all Remedium HMS models.
    Provides soft delete capabilities and standard timestamps.
    """

    created_at = models.DateTimeField(auto_now_add=True, db_index=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    is_deleted = models.BooleanField(default=False, db_index=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    # Standard manager filters out deleted records by default
    objects = SoftDeleteManager()
    # All records manager includes deleted records
    all_objects = SoftDeleteManager(alive_only=False)

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        """Soft delete a single record."""
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save(using=using, update_fields=["is_deleted", "deleted_at"])

    def restore(self):
        """Restore a soft-deleted record."""
        self.is_deleted = False
        self.deleted_at = None
        self.save(update_fields=["is_deleted", "deleted_at"])

    def hard_delete(self, using=None, keep_parents=False):
        """Permanently delete a single record."""
        return super().delete(using=using, keep_parents=keep_parents)
