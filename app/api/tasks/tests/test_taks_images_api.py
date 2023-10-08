from api.tasks.views import CreateTaskImage, DeleteTaskImage, ListTaskImages
from backend.tasks.tests.utils import TaskImageTestUtils, TaskTestUtils
from backend.users.tests.utils import UserTestUtils
from django.conf import settings
from rest_framework import status
from rest_framework.test import APITestCase

TASKS_IMAGE_API_URL = "/api/v1/tasks/image/"


class DeleteTaskImageTestCase(APITestCase):
    endpoint_url_tmp = "%(TASKS_IMAGE_API_URL)sdelete/%(task_uuid)s/"
    TEST_UUID = "ed7358e8-9c1c-4457-b0af-ee652c9c8cf9"

    @property
    def endpoint_url(self):
        return self.endpoint_url_tmp % {
            "TASKS_IMAGE_API_URL": TASKS_IMAGE_API_URL,
            "task_uuid": self.TEST_UUID,
        }

    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = UserTestUtils.create(username="admin", email="admin@example.com")

    def test_view_url(self):
        response = self.client.delete(self.endpoint_url)
        self.assertNotEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIs(response.resolver_match.func.view_class, DeleteTaskImage)

    def test_login_required(self):
        response = self.client.delete(self.endpoint_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_method_is_not_allowed(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.endpoint_url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_patch_method_is_not_allowed(self):
        self.client.force_authenticate(self.user)
        response = self.client.patch(self.endpoint_url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_post_method_is_not_allowed(self):
        self.client.force_authenticate(self.user)
        response = self.client.post(self.endpoint_url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_put_method_is_not_allowed(self):
        self.client.force_authenticate(self.user)
        response = self.client.put(self.endpoint_url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_response_type_is_json(self):
        response = self.client.delete(self.endpoint_url)
        self.assertEqual(response["Content-Type"], "application/json")

    def test_integration_with_delete_task_service(self):
        task = TaskTestUtils.create(
            uuid=self.TEST_UUID, title="Task to delete", owner_id=self.user.id
        )
        TaskImageTestUtils.create(uuid=self.TEST_UUID, task_id=task.id)
        self.client.force_authenticate(self.user)
        response = self.client.delete(self.endpoint_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIsNone(TaskImageTestUtils.first(uuid=self.TEST_UUID))


class CreateTaskImageTestCase(APITestCase):
    endpoint_url_tmp = "%(TASKS_IMAGE_API_URL)screate/%(task_uuid)s/"
    TEST_UUID = "ed7358e8-9c1c-4457-b0af-ee652c9c8cf9"

    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = UserTestUtils.create(username="admin", email="admin@example.com")

    @property
    def endpoint_url(self):
        return self.endpoint_url_tmp % {
            "TASKS_IMAGE_API_URL": TASKS_IMAGE_API_URL,
            "task_uuid": self.TEST_UUID,
        }

    def test_view_url(self):
        self.client.force_authenticate(self.user)
        response = self.client.post(self.endpoint_url)
        self.assertNotEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIs(response.resolver_match.func.view_class, CreateTaskImage)

    def test_get_method_is_not_allowed(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.endpoint_url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_patch_method_is_not_allowed(self):
        self.client.force_authenticate(self.user)
        response = self.client.patch(self.endpoint_url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_put_method_is_not_allowed(self):
        self.client.force_authenticate(self.user)
        response = self.client.put(self.endpoint_url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_method_is_not_allowed(self):
        self.client.force_authenticate(self.user)
        response = self.client.delete(self.endpoint_url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_login_required(self):
        response = self.client.post(self.endpoint_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_response_type_is_json(self):
        response = self.client.post(self.endpoint_url)
        self.assertEqual(response["Content-Type"], "application/json")

    def test_integration_create_task_image(self):
        task = TaskTestUtils.create(
            uuid=self.TEST_UUID, owner_id=self.user.id, title="my task with image"
        )
        image = TaskImageTestUtils.simple_uploaded_image()
        data = {"image": image}
        self.client.force_authenticate(self.user)
        response = self.client.post(
            self.endpoint_url,
            data,
            format="multipart",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        task_image = TaskImageTestUtils.first(task_id=task.id)
        self.assertIsNotNone(task_image)
        self.assertEqual(
            task_image.image.read(), TaskImageTestUtils.simple_uploaded_image().read()
        )
        expected_url = f"{settings.MEDIA_URL}{settings.UPLOAD_IMAGES_PATH}{task.uuid}/{task_image.uuid}.jpeg"
        self.assertEqual(response.json().get("image"), expected_url)


class ListTaskImageViewTestCase(APITestCase):
    endpoint_url_tmp = "%(TASKS_IMAGE_API_URL)slist/%(task_uuid)s/"
    TEST_UUID = "ed7358e8-9c1c-4457-b0af-ee652c9c8cf9"

    @property
    def endpoint_url(self):
        return self.endpoint_url_tmp % {
            "TASKS_IMAGE_API_URL": TASKS_IMAGE_API_URL,
            "task_uuid": self.TEST_UUID,
        }

    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = UserTestUtils.create(username="admin", email="admin@example.com")

    def test_view_url(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.endpoint_url)
        self.assertNotEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIs(response.resolver_match.func.view_class, ListTaskImages)

    def test_post_method_is_not_allowed(self):
        self.client.force_authenticate(self.user)
        response = self.client.post(self.endpoint_url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_put_method_is_not_allowed(self):
        self.client.force_authenticate(self.user)
        response = self.client.put(self.endpoint_url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_patch_method_is_not_allowed(self):
        self.client.force_authenticate(self.user)
        response = self.client.patch(self.endpoint_url)
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

    def test_integration_with_service(self):
        uuids = [
            "fbb45ef5-6d46-435c-9eef-e39783a5abbb",
            "ed7358e8-9c1c-4457-b0af-ee652c9c8cf9",
        ]

        task = TaskTestUtils.create(
            title="My test task", owner_id=self.user.id, uuid=self.TEST_UUID
        )
        TaskImageTestUtils.create(task_id=task.id, uuid=uuids[0])
        TaskImageTestUtils.create(task_id=task.id, uuid=uuids[1])
        TaskImageTestUtils.create()

        self.client.force_authenticate(self.user)
        response = self.client.get(self.endpoint_url)
        response_data = response.json()
        response_keys = list(response_data[0].keys())
        expected_keys = ["uuid", "image"]
        self.assertListEqual(response_keys, expected_keys)

        expected_tasks_images_uuids = [uuids[0], uuids[1]]
        retrieved_tasks_images_uuids = [image.get("uuid") for image in response.json()]
        self.assertListEqual(retrieved_tasks_images_uuids, expected_tasks_images_uuids)
