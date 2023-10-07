from http import HTTPStatus

from backend.tasks.tests.utils import TaskImageTestUtils, TaskTestUtils
from backend.users.tests.utils import UserTestUtils
from django.test import TestCase
from django.urls import reverse
from frontend.tasks.views import CreateTaskImage, DeleteTaskImage


class CreateTaskImageViewTestCase(TestCase):
    test_uuid = "21fb4127-c9e6-4040-8684-dceeeb8eb816"
    view_url = f"/tasks/images/create/{test_uuid}/"
    view_name = "tasks_image_create"

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.user = UserTestUtils.create()

    def test_view_url(self):
        response = self.client.post(self.view_url)
        self.assertNotEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertIs(response.resolver_match.func.view_class, CreateTaskImage)

    def test_view_name(self):
        url = reverse(self.view_name, args=[self.test_uuid])
        response = self.client.post(url)
        self.assertNotEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertIs(response.resolver_match.func.view_class, CreateTaskImage)

    def test_login_required(self):
        response = self.client.post(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_non_existent_task_uuid_returns_400(self):
        self.client.force_login(self.user)
        image = TaskImageTestUtils.simple_uploaded_image()
        response = self.client.post(
            self.view_url, data={"image": image}, format="multipart"
        )
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_no_task_owner_cannot_add_images_to_task(self):
        TaskTestUtils.create(title="My task", uuid=self.test_uuid)
        image = TaskImageTestUtils.simple_uploaded_image()

        self.client.force_login(self.user)
        response = self.client.post(
            self.view_url, data={"image": image}, format="multipart"
        )
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_task_owner_can_add_images_to_task(self):
        TaskTestUtils.create(
            title="My task", uuid=self.test_uuid, owner_id=self.user.id
        )
        image = TaskImageTestUtils.simple_uploaded_image()

        self.client.force_login(self.user)
        response = self.client.post(
            self.view_url, data={"image": image}, format="multipart"
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertIsNotNone(
            TaskImageTestUtils.first(
                task__uuid=self.test_uuid, task__owner_id=self.user.id
            )
        )


class DeleteTaskImageViewTestCase(TestCase):
    test_uuid = "21fb4127-c9e6-4040-8684-dceeeb8eb816"
    view_url = f"/tasks/images/delete/{test_uuid}/"
    view_name = "tasks_image_delete"

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.user = UserTestUtils.create()

    def test_view_url(self):
        self.client.force_login(self.user)
        response = self.client.get(self.view_url)
        self.assertNotEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertIs(response.resolver_match.func.view_class, DeleteTaskImage)

    def test_view_name(self):
        self.client.force_login(self.user)
        url = reverse(self.view_name, args=[self.test_uuid])
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertIs(response.resolver_match.func.view_class, DeleteTaskImage)

    def test_login_required(self):
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_non_existent_task_image_uuid_returns_400(self):
        self.client.force_login(self.user)
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_non_task_owner_cannot_delete_task_image(self):
        TaskImageTestUtils.create(uuid=self.test_uuid)
        self.client.force_login(self.user)
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_user_can_delete_task_image(self):
        task = TaskTestUtils.create(
            title="My Task", owner_id=self.user.id, uuid=self.test_uuid
        )
        TaskImageTestUtils.create(uuid=self.test_uuid, task_id=task.id)
        self.assertIsNotNone(TaskImageTestUtils.first(uuid=self.test_uuid))
        self.client.force_login(self.user)
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIsNone(TaskImageTestUtils.first(uuid=self.test_uuid))
