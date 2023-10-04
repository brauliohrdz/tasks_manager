from backend.users.auth_services import token_for_user_with
from backend.users.tests.utils import TokenTestUtils, UserTestUtils
from django.core.exceptions import PermissionDenied
from django.test import TestCase


class TokenForUserTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.user = UserTestUtils.create(username="homerjay", password="test1234")

    def test_username_is_required(self):
        with self.assertRaisesMessage(AssertionError, "username is required."):
            token_for_user_with(username="", password="random-pass")

    def test_password_is_required(self):
        with self.assertRaisesMessage(AssertionError, "password is required."):
            token_for_user_with(username="homerjay", password="")

    def test_wrong_credentials_raises_exception(self):
        with self.assertRaisesMessage(
            PermissionDenied, "Incorrect username or password"
        ):
            token_for_user_with(username="homerjay", password="test123")

    def test_token_for_user_with(self):
        token = TokenTestUtils.create(user_id=self.user.id)
        retrieved_token = token_for_user_with(username="homerjay", password="test1234")
        self.assertEqual(token.key, retrieved_token)
