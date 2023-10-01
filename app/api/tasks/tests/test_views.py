from api.tasks.views import TasksList
from django.contrib.auth.models import User
from mock import patch
from rest_framework import status
from rest_framework.test import APITestCase


class TasksListViewTextCase(APITestCase):
    endpoint_url = "/api/v1/tasks/list/"

    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = User.objects.create(username="admin", email="admin@example.com")

    def test_view_url(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.endpoint_url)
        self.assertNotEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIs(response.resolver_match.func.view_class, TasksList)

    def test_post_method_is_not_allowed(self):
        self.client.force_authenticate(self.user)
        response = self.client.post(self.endpoint_url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_put_method_is_not_allowed(self):
        self.client.force_authenticate(self.user)
        response = self.client.put(self.endpoint_url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_method_is_not_allowed(self):
        self.client.force_authenticate(self.user)
        response = self.client.delete(self.endpoint_url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_login_is_required(self):
        response = self.client.get(self.endpoint_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_response_type_is_json(self):
        response = self.client.get(self.endpoint_url)
        self.assertEqual(response["Content-Type"], "application/json")

    def test_response_has_expected_structure(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.endpoint_url)

        response_data = response.json()
        self.assertIs(type(response_data), list)
        response_task_item_keys = list(response_data[0].keys())
        tasks_list_expected_item_keys = ["title", "created", "expires", "status"]

        self.assertListEqual(tasks_list_expected_item_keys, response_task_item_keys)

    @patch("api.tasks.views.list_tasks_for")
    def test_tasks_list_service_call(self, mock_service):
        self.client.force_authenticate(self.user)
        self.client.get(self.endpoint_url)
        mock_service.assert_called_once_with(user_id=self.user.id)
