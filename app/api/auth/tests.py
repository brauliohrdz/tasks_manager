from api.auth.views import AuthTokenView
from backend.users.tests.utils import TokenTestUtils, UserTestUtils
from rest_framework import status
from rest_framework.test import APITestCase


class AuthTokenViewTestCase(APITestCase):
    endpoint_url = "/api/v1/auth/token/"

    def test_view_url(self):
        response = self.client.post(self.endpoint_url)
        self.assertNotEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIs(response.resolver_match.func.view_class, AuthTokenView)

    def test_invalid_credentials_gets_400(self):
        data = {"username": "fake_username", "password": "test1234"}
        response = self.client.post(self.endpoint_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        expected_error = "Incorrect username or password."
        retrieved_error = response.json().get("error")
        self.assertEqual(expected_error, retrieved_error)

    def test_username_is_required(self):
        data = {"username": "", "password": "test1234"}
        response = self.client.post(self.endpoint_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        expected_error = "Este campo no puede estar en blanco."
        retrieved_error = response.json().get("error").get("username")[0]
        self.assertEqual(expected_error, retrieved_error)

    def test_password_is_required(self):
        data = {"username": "fake_username", "password": ""}
        response = self.client.post(self.endpoint_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        expected_error = "Este campo no puede estar en blanco."
        retrieved_error = response.json().get("error").get("password")[0]
        self.assertEqual(expected_error, retrieved_error)

    def test_auth_token_view(self):
        TEST_USERNAME = "homerjay"
        TEST_PASSWORD = "test_1234"
        user = UserTestUtils.create(username=TEST_USERNAME, password=TEST_PASSWORD)
        token = TokenTestUtils.create(user_id=user.id)
        data = {"username": TEST_USERNAME, "password": TEST_PASSWORD}

        response = self.client.post(self.endpoint_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get("token"), token.key)
