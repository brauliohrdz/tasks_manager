from backend.tasks.services import (
    create_task_image,
    delete_task_image,
    get_task_image_for_owner,
)
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase

from .utils import TaskImageTestUtils, TaskTestUtils


class BaseTaskImageTestCase(TestCase):
    TEST_UUID = "ed7358e8-9c1c-4457-b0af-ee652c9c8cf9"

    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = User.objects.create(username="homerjay@example.com")
        cls.task = TaskTestUtils.create(title="Mi task", owner_id=cls.user.id)
        cls.task_image = TaskImageTestUtils.create(task_id=cls.task.id)
        return super().setUpTestData()


class DeleteTaskImageTestCase(BaseTaskImageTestCase):
    def test_task_uuid_is_required(self):
        with self.assertRaisesMessage(AssertionError, "TaskImage uuid is required."):
            delete_task_image(task_image_uuid="", owner_id=1)

    def test_task_owner_is_required(self):
        with self.assertRaisesMessage(AssertionError, "Owner id is required."):
            delete_task_image(task_image_uuid=self.TEST_UUID, owner_id="")

    def test_only_task_owner_can_delete_task(self):
        no_owned_task_image = TaskImageTestUtils.create()
        with self.assertRaisesMessage(PermissionError, "User is not image owner."):
            delete_task_image(
                task_image_uuid=no_owned_task_image.uuid, owner_id=self.user.id
            )

    def test_non_existent_uuid_raises_exception(self):
        non_existent_uuid = "f9fa2e26-6c95-4cc8-ad70-707ace27c26a"
        with self.assertRaisesMessage(
            ObjectDoesNotExist, "TaskImage matching query does not exist."
        ):
            delete_task_image(task_image_uuid=non_existent_uuid, owner_id=self.user.id)

    def test_task_delete(self):
        my_task = TaskTestUtils.create(title="My task", owner_id=self.user.id)
        TaskImageTestUtils.create(task_id=my_task.id)
        task_image_to_delete = TaskImageTestUtils.create()
        tasks_images_in_database = TaskImageTestUtils.count()
        self.assertEqual(tasks_images_in_database, 3)
        delete_task_image(
            task_image_uuid=task_image_to_delete.uuid,
            owner_id=task_image_to_delete.owner_id,
        )

        tasks_in_database = TaskImageTestUtils.count()
        self.assertEqual(tasks_in_database, 2)
        self.assertIsNone(TaskImageTestUtils.first(uuid=task_image_to_delete.uuid))


class GetTaskImageForOwnerTestCase(BaseTaskImageTestCase):
    def test_task_uuid_is_required(self):
        with self.assertRaisesMessage(AssertionError, "TaskImage uuid is required."):
            get_task_image_for_owner(task_image_uuid="", owner_id=self.user.id)

    def test_task_owner_is_required(self):
        with self.assertRaisesMessage(AssertionError, "Owner id is required."):
            get_task_image_for_owner(task_image_uuid=self.task_image.uuid, owner_id="")

    def test_non_existent_task_image_uuid_raises_exception(self):
        non_existent_uuid = "f9fa2e26-6c95-4cc8-ad70-707ace27c26a"
        with self.assertRaisesMessage(
            ObjectDoesNotExist, "TaskImage matching query does not exist."
        ):
            get_task_image_for_owner(
                task_image_uuid=non_existent_uuid, owner_id=self.user.id
            )

    def test_only_task_owner_can_get_images(self):
        no_owned_task_image = TaskImageTestUtils.create()
        with self.assertRaisesMessage(PermissionError, "User is not image owner."):
            get_task_image_for_owner(
                task_image_uuid=no_owned_task_image.uuid, owner_id=self.user.id
            )

    def test_get_image_for_owner(self):
        pass


class AddTaskImageTestCase(BaseTaskImageTestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.image = TaskImageTestUtils.simple_uploaded_image(name="my-test-image.jpg")

    def test_task_uuid_is_required(self):
        with self.assertRaisesMessage(AssertionError, "Task uuid is required."):
            create_task_image(task_uuid="", owner_id=self.user.id, image=self.image)

    def test_task_owner_is_required(self):
        with self.assertRaisesMessage(AssertionError, "Owner id is required."):
            create_task_image(task_uuid=self.task.uuid, owner_id="", image=self.image)

    def test_non_existent_task_uuid_raises_exception(self):
        non_existent_uuid = "f9fa2e26-6c95-4cc8-ad70-707ace27c26a"
        with self.assertRaisesMessage(
            ObjectDoesNotExist, "Task matching query does not exist."
        ):
            create_task_image(
                task_uuid=non_existent_uuid, owner_id=self.user.id, image=self.image
            )

    def test_only_task_owner_can_add_images(self):
        no_owned_task = TaskTestUtils.create(title="no owned task")
        with self.assertRaisesMessage(PermissionError, "User is not task owner."):
            create_task_image(
                task_uuid=no_owned_task.uuid, owner_id=self.user.id, image=self.image
            )

    def test_add_task_image(self):
        task_image = create_task_image(
            task_uuid=self.task.uuid, owner_id=self.user.id, image=self.image
        )

        task_image = TaskImageTestUtils.first(
            uuid=task_image.uuid, task_id=self.task.id
        )
        self.assertIsNotNone(task_image)
        self.assertEqual(
            task_image.image.read(), TaskImageTestUtils.simple_uploaded_image().read()
        )
