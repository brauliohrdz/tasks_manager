from api.tasks.views import TasksList
from rest_framework import status
from rest_framework.test import APITestCase


class TasksListViewTextCase(APITestCase):
    endpoint_url = "/api/v1/tasks/list/"

    def test_view_url(self):
        response = self.client.get(self.endpoint_url)
        self.assertNotEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIs(response.resolver_match.func.view_class, TasksList)

    def test_post_method_is_not_allowed(self):
        response = self.client.post(self.endpoint_url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_put_method_is_not_allowed(self):
        response = self.client.put(self.endpoint_url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_method_is_not_allowed(self):
        response = self.client.delete(self.endpoint_url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
