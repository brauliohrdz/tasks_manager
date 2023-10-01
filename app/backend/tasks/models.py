from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class Task(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    expires = models.DateTimeField(null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    owner = models.ForeignKey(User, related_name="tasks", on_delete=models.PROTECT)

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

    STATUS_CHOICES = (
        (PENDING, _("Pendiente")),
        (IN_PROGRESS, _("En progreso")),
        (COMPLETED, _("Completada")),
    )
    status = models.CharField(choices=STATUS_CHOICES, max_length=20)

    class Meta:
        verbose_name = "Task"
        verbose_name_plural = "Tasks"
