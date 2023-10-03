from uuid import uuid4

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class Task(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True, editable=False)
    expires = models.DateTimeField(null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    owner = models.ForeignKey(
        User, related_name="tasks", on_delete=models.PROTECT, editable=False
    )

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

    STATUS_CHOICES = (
        (PENDING, _("Pendiente")),
        (IN_PROGRESS, _("En progreso")),
        (COMPLETED, _("Completada")),
    )
    status = models.CharField(choices=STATUS_CHOICES, max_length=20)

    @classmethod
    def editable_fields(cls) -> list[str]:
        editable_fields = list(
            filter(lambda f: f.editable and not f.primary_key, cls._meta.fields)
        )
        return [field.name for field in editable_fields]

    class Meta:
        verbose_name = "Task"
        verbose_name_plural = "Tasks"
