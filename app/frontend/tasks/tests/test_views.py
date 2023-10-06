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

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.user = UserTestUtils.create()

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

    def test_non_existent_task_uuid_returns_404(self):
        self.client.force_login(self.user)
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        response = self.client.post(self.view_url, data={"title": "foo title"})

    def test_non_task_owner_cannot_accest_to_task_data(self):
        TaskTestUtils.create(title="My Task", uuid=self.test_uuid)
        self.client.force_login(self.user)
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_non_task_owner_cannot_modify_task(self):
        TaskTestUtils.create(title="My Task", uuid=self.test_uuid)
        self.client.force_login(self.user)
        data = {"title": "My task title"}
        response = self.client.post(self.view_url, data=data)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_user_can_access_to_own_task(self):
        TaskTestUtils.create(
            title="My Task", owner_id=self.user.id, uuid=self.test_uuid
        )
        post_data = {
            "title": "Mi updated title",
            "description": "Mi description",
            "status": "completed",
            "expires": "2025-01-01",
        }

        self.client.force_login(self.user)
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.OK, msg="GET")
        response = self.client.post(self.view_url, data=post_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND, msg="POST")

    def test_user_can_update_its_own_task(self):
        task = TaskTestUtils.create(
            title="My Task", owner_id=self.user.id, uuid=self.test_uuid
        )

        post_data = {
            "title": "Mi updated title",
            "description": "Mi description",
            "status": "completed",
            "expires": "2025-01-01",
        }

        self.client.force_login(self.user)
        response = self.client.post(self.view_url, data=post_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        task.refresh_from_db()
        self.assertEqual(task.title, post_data.get("title"))
        self.assertEqual(task.description, post_data.get("description"))
        self.assertEqual(task.status, post_data.get("status"))
        self.assertEqual(task.expires.strftime("%Y-%m-%d"), post_data.get("expires"))
