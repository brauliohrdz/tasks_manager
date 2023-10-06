from http import HTTPStatus

from backend.tasks.tests.utils import TaskTestUtils
from backend.users.tests.utils import UserTestUtils
from django.test import TestCase
from django.urls import reverse
from frontend.tasks.views import CreateTask, TasksList, UpdateTask


class TasksListViewTestCase(TestCase):
    view_url = "/tasks/"
    view_name = "tasks_list"
    template = "tasks_list.html"

    def test_view_url(self):
        response = self.client.get(self.view_url)
        self.assertNotEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertIs(response.resolver_match.func.view_class, TasksList)

    def test_view_name(self):
        url = reverse(self.view_name)
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertIs(response.resolver_match.func.view_class, TasksList)

    def test_login_required(self):
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_list_user_tasks_only(self):
        user = UserTestUtils.create()
        TaskTestUtils.create(owner_id=user.id, title="my_task_1")
        TaskTestUtils.create(owner_id=user.id, title="my_task_2")
        TaskTestUtils.create(title="not-my-task")

        self.client.force_login(user)
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        tasks = response.context.get("tasks")
        tasks_titles = [task.title for task in tasks]
        self.assertEqual(len(tasks_titles), 2)
        self.assertListEqual(["my_task_1", "my_task_2"], tasks_titles)


class CreateTaskViewTestCase(TestCase):
    view_url = "/tasks/create/"
    view_name = "tasks_create"
    template = "tasks_form.html"

    def test_view_url(self):
        response = self.client.get(self.view_url)
        self.assertNotEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertIs(response.resolver_match.func.view_class, CreateTask)

    def test_view_name(self):
        url = reverse(self.view_name)
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertIs(response.resolver_match.func.view_class, CreateTask)

    def test_login_required(self):
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)


class UpdateTaskViewTestCase(TestCase):
    test_uuid = "21fb4127-c9e6-4040-8684-dceeeb8eb816"
    view_url = f"/tasks/update/{test_uuid}/"
    view_name = "tasks_update"
    template = "tasks_form.html"

    def test_view_url(self):
        response = self.client.get(self.view_url)
        self.assertNotEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertIs(response.resolver_match.func.view_class, UpdateTask)

    def test_view_name(self):
        url = reverse(self.view_name, args=[self.test_uuid])
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertIs(response.resolver_match.func.view_class, UpdateTask)

    def test_login_required(self):
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
