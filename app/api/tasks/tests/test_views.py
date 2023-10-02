from api.tasks.views import TasksList
from backend.tasks.tests.utils import TaskTestUtils
from django.contrib.auth.models import User
from freezegun import freeze_time
from mock import patch
from rest_framework import status
from rest_framework.test import APITestCase


class TasksListViewTextCase(APITestCase):
    endpoint_url = "/api/v1/tasks/list/"

    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = User.objects.create(username="admin", email="admin@example.com")

    @property
    def service_mock_data(self):
        return [
            {
                "uuid": "fbb45ef5-6d46-435c-9eef-e39783a5abbb",
                "title": "Mi Task Title",
                "created": "01-01-2022 12:00:00",
                "expires": "01-01-2022 12:00:00",
                "status": "pending",
            }
        ]

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

    @patch("api.tasks.views.list_tasks_for_user")
    def test_response_has_expected_structure(self, mock_service):
        mock_service.return_value = self.service_mock_data

        self.client.force_authenticate(self.user)
        response = self.client.get(self.endpoint_url)

        response_data = response.json()
        self.assertIs(type(response_data), list)
        response_task_item_keys = list(response_data[0].keys())
        tasks_list_expected_item_keys = [
            "uuid",
            "title",
            "created",
            "expires",
            "status",
        ]

        self.assertListEqual(tasks_list_expected_item_keys, response_task_item_keys)

    @patch("api.tasks.views.list_tasks_for_user")
    def test_tasks_list_service_call(self, mock_service):
        self.client.force_authenticate(self.user)
        self.client.get(self.endpoint_url)
        mock_service.assert_called_once_with(id=self.user.id)

    @patch("api.tasks.views.list_tasks_for_user")
    def test_tasks_list(self, mock_service):
        mock_service.return_value = self.service_mock_data

        self.client.force_authenticate(self.user)
        response = self.client.get(self.endpoint_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertListEqual(response.json(), self.service_mock_data)

    @freeze_time("2022-01-01 12:00:00")
    def test_integration_with_service(self):
        uuids = [
            "fbb45ef5-6d46-435c-9eef-e39783a5abbb",
            "ed7358e8-9c1c-4457-b0af-ee652c9c8cf9",
            "3003a10f-3175-47f1-b404-eeee027102de",
        ]
        TaskTestUtils.create(uuid=uuids[0], title="Mi Task1", owner=self.user)
        TaskTestUtils.create(uuid=uuids[1], title="Mi Task2", owner=self.user)
        TaskTestUtils.create(uuid=uuids[2], title="THIS TASK SHOULDN'T BE LISTED")

        self.client.force_authenticate(self.user)
        response = self.client.get(self.endpoint_url)

        expected_tasks = [
            {
                "uuid": uuids[0],
                "title": "Mi Task1",
                "created": "01-01-2022 12:00:00",
                "expires": None,
                "status": "",
            },
            {
                "uuid": uuids[1],
                "title": "Mi Task2",
                "created": "01-01-2022 12:00:00",
                "expires": None,
                "status": "",
            },
        ]
        retrieved_tasks = response.json()
        self.assertEqual(len(retrieved_tasks), len(retrieved_tasks))
        for retrieved_task_data, expected_task_data in zip(
            retrieved_tasks, expected_tasks
        ):
            self.assertDictEqual(retrieved_task_data, expected_task_data)
