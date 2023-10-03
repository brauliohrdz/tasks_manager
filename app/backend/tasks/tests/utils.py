import random
import string
from typing import Optional

from backend.tasks.models import Task
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
    def create(cls, title: str, owner: Optional[User] = None, **kwargs):
        owner = owner or cls._create_random_owner()
        return Task.objects.create(title=title, owner=owner, **kwargs)

    @classmethod
    def get(cls, **kwargs):
        return Task.objects.filter(**kwargs).first()

    @classmethod
    def count(cls, **kwargs):
        return Task.objects.filter(**kwargs).count()
