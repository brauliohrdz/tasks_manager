import random
import string
from typing import Optional

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class UserTestUtils:
    @classmethod
    def random_username(cls):
        RANDOM_USERNAME_SIZE = 10
        characters = string.ascii_letters + string.digits
        return "".join(random.choice(characters) for _ in range(RANDOM_USERNAME_SIZE))

    @classmethod
    def create(
        cls,
        username: Optional[str] = None,
        email: Optional[str] = None,
        password: Optional[str] = None,
        **kwargs,
    ):
        username = username or cls.random_username()
        email = email or f"{username}@example.com"
        password = password or "test1234"
        user = User(username=username, email=email, **kwargs)
        user.set_password(password)
        user.save()
        return user


class TokenTestUtils:
    @classmethod
    def create(cls, user_id: Optional[int] = None, **kwargs):
        user_id = user_id or UserTestUtils.crete().id
        return Token.objects.create(user_id=user_id)
