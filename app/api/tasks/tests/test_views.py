from api.tasks.views import TasksList
from rest_framework import status
from rest_framework.test import APITestCase


class TasksListViewTextCase(APITestCase):
    endpoint_url = "/api/v1/tasks/list/"

    def test_view_url(self):
        response = self.client.get(self.endpoint_url)
        self.assertNotEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIs(response.resolver_match.func.view_class, TasksList)
