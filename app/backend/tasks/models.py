import os
from uuid import uuid4

from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import FieldError
from django.db import models


class Task(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True, editable=False)
    expires = models.DateTimeField(null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    owner = models.ForeignKey(User, related_name="tasks", on_delete=models.PROTECT)

    class StatusChoices(models.TextChoices):
        PENDING = "pending", "Pending"
        IN_PROGRESS = "in_progress", "In Progress"
        COMPLETED = "completed", "Completed"

    status = models.CharField(choices=StatusChoices.choices, max_length=20)

    @classmethod
    def get_editable_fields(cls) -> list[str]:
        field_is_editable = lambda f: f.editable and not f.primary_key  # noqa: E731
        editable_fields = list(filter(field_is_editable, cls._meta.fields))
        return [field.name for field in editable_fields]

    def validate_fields_are_editable(self, fields: list[str]) -> bool:
        editable_fields = self.get_editable_fields()
        all_fields_are_editable = all([field in editable_fields for field in fields])
        if not all_fields_are_editable:
            raise FieldError("Some fields cannot be updated.")

    def set_fields(self, **kwargs):
        updated_fields = []
        for field, value in kwargs.items():
            setattr(self, field, value)
            updated_fields.append(field)

    class Meta:
        verbose_name = "Task"
        verbose_name_plural = "Tasks"


class TaskImage(models.Model):
    def image_name(self, filename):
        extension = filename.split(".")[-1]
        task_folder = str(self.task.uuid)
        image_filename = f"{self.uuid}.{extension}"
        return os.path.join(settings.UPLOAD_IMAGES_PATH, task_folder, image_filename)

    uuid = models.UUIDField(unique=True, default=uuid4, editable=False)
    task = models.ForeignKey(Task, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to=image_name)

    @property
    def owner_id(self):
        return self.task.owner_id

    class Meta:
        verbose_name = "TaskImage"
        verbose_name_plural = "TaskImages"
