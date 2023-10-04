from django.contrib.auth import authenticate
from django.core.exceptions import PermissionDenied
from rest_framework.authtoken.models import Token


def token_for_user_with(username: str, password: str) -> str:
    assert username, "username is required."
    assert password, "password is required."
    user = authenticate(username=username, password=password)
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return token.key
    raise PermissionDenied("Incorrect username or password.")
