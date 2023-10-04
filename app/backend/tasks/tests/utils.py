import random
import string
from io import BytesIO
from typing import Optional
from uuid import uuid4

from backend.tasks.models import Task, TaskImage
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image


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
    TEST_IMAGE_CONTENT = b"image_simulated_content"

    @staticmethod
    def simple_uploaded_image(
        name: Optional[str] = None,
    ):
        name = name or "test_image.jpeg"
        content = BytesIO()
        img = Image.new("RGB", (100, 100))
        img.save(content, "jpeg")
        content_type = "image/jpeg"
        return SimpleUploadedFile(name, content.getvalue(), content_type=content_type)

    @classmethod
    def create(
        cls,
        task_id: Optional[int] = None,
        image: Optional[SimpleUploadedFile] = None,
        uuid: Optional[str] = None,
    ):
        image = image or cls.simple_uploaded_image()
        task_id = task_id or TaskTestUtils.create(title="my random task").id
        uuid = uuid or uuid4()
        return TaskImage.objects.create(uuid=uuid, task_id=task_id, image=image)

    @classmethod
    def first(cls, **kwargs):
        return TaskImage.objects.filter(**kwargs).first()

    @classmethod
    def count(cls, **kwargs):
        return TaskImage.objects.filter(**kwargs).count()
