import random
import string
from typing import Optional

from backend.tasks.models import Task, TaskImage
from django.contrib.auth.models import User


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
