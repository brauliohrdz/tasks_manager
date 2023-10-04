import random
import string
from typing import Optional

from backend.tasks.models import Task, TaskImage
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile


class TaskTestUtils:
    @classmethod
    def _generate_username(cls):
        RANDOM_USERNAME_SIZE = 10
        return "".join(
            random.choice(string.ascii_lowercase) for _ in range(RANDOM_USERNAME_SIZE)
        )

    @classmethod
    def _create_random_owner(cls):
        username = cls._generate_username()
        email = f"{username}@example.com"
        return User.objects.create(username=username, email=email)

    @classmethod
    def create(cls, title: str, owner_id: Optional[User] = None, **kwargs):
        owner_id = owner_id or cls._create_random_owner().id
        return Task.objects.create(title=title, owner_id=owner_id, **kwargs)

    @classmethod
    def first(cls, **kwargs):
        return Task.objects.filter(**kwargs).first()

    @classmethod
    def count(cls, **kwargs):
        return Task.objects.filter(**kwargs).count()


class TaskImageTestUtils:
    TEST_IMAGE_CONTENT = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x00\x00\x00\xc0\xbd\xa5\x9e\x00\x00\x00\x0bIDAT\x08\xd7c\xfc\xff\xff?\x00\x05\x00\x01\r\n\x00\x00\x00\x00IEND\xaeB`\x82"

    @staticmethod
    def simple_uploaded_image(
        name: Optional[str] = None,
        content: Optional[str] = None,
        content_type: Optional[str] = None,
    ):
        name = name or "test_image.png"
        content = content or TaskImageTestUtils.TEST_IMAGE_CONTENT
        content_type = content_type or "image/png"
        return SimpleUploadedFile(name, content, content_type=content_type)

    @classmethod
    def _create_random_owner(cls):
        username = cls._generate_username()
        email = f"{username}@example.com"
        return User.objects.create(username=username, email=email)

    @classmethod
    def create(cls, image, task_id: str, owner_id: Optional[User] = None):
        owner_id = owner_id or cls._create_random_owner().id
        return TaskImage.objects.create(task_id, owner_id=owner_id, image=image)

    @classmethod
    def first(cls, **kwargs):
        return TaskImage.objects.filter(**kwargs).first()

    @classmethod
    def count(cls, **kwargs):
        return TaskImage.objects.filter(**kwargs).count()
