import shutil

from backend.tasks.services import (
    create_task,
    create_task_image,
    delete_task,
    get_task_image_for_owner,
    list_tasks_for_user,
    update_task,
)
from django.contrib.auth.models import User
from django.core.exceptions import FieldError, ObjectDoesNotExist, ValidationError
from django.db.models import QuerySet
from django.test import TestCase
from django.utils import timezone

from .utils import TaskImageTestUtils, TaskTestUtils


class GetTaskImageForOwnerTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = User.objects.create(username="homerjay@example.com")
        cls.task = TaskTestUtils.create(title="My Task", owner_id=cls.user.id)
        cls.task_image = TaskImageTestUtils.create(task_id=cls.task.id)

        return super().setUpTestData()

    @classmethod
    def tearDownClass(cls) -> None:
        shutil.rmtree("images/", ignore_errors=True)
        super().tearDownClass()

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


class AddTaskImageTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = User.objects.create(username="homerjay@example.com")
        cls.task = TaskTestUtils.create(title="My Task", owner_id=cls.user.id)
        cls.image = TaskImageTestUtils.simple_uploaded_image()

        return super().setUpTestData()

    @classmethod
    def tearDownClass(cls) -> None:
        shutil.rmtree("images/", ignore_errors=True)
        super().tearDownClass()

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


class DeleteTaskTestCase(TestCase):
    TEST_UUID = "ed7358e8-9c1c-4457-b0af-ee652c9c8cf9"

    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = User.objects.create(username="homerjay@example.com")
        return super().setUpTestData()

    def test_task_uuid_is_required(self):
        with self.assertRaisesMessage(AssertionError, "Task uuid is required."):
            delete_task(task_uuid="", owner_id=1)

    def test_task_owner_is_required(self):
        with self.assertRaisesMessage(AssertionError, "Owner id is required."):
            delete_task(task_uuid=self.TEST_UUID, owner_id="")

    def test_only_task_owner_can_delete_task(self):
        no_owned_task = TaskTestUtils.create(title="My task for delete")
        with self.assertRaisesMessage(PermissionError, "User is not task owner"):
            delete_task(task_uuid=no_owned_task.uuid, owner_id=self.user.id)

    def test_non_existent_uuid_raises_exception(self):
        non_existent_uuid = "f9fa2e26-6c95-4cc8-ad70-707ace27c26a"
        with self.assertRaisesMessage(
            ObjectDoesNotExist, "Task matching query does not exist."
        ):
            delete_task(task_uuid=non_existent_uuid, owner_id=self.user.id)

    def test_task_delete(self):
        TaskTestUtils.create(title="My task", owner_id=self.user.id)
        task_to_delete = TaskTestUtils.create(title="task_to_delete")
        tasks_in_database = TaskTestUtils.count()
        self.assertEqual(tasks_in_database, 2)
        delete_task(task_uuid=task_to_delete.uuid, owner_id=task_to_delete.owner_id)

        tasks_in_database = TaskTestUtils.count()
        self.assertEqual(tasks_in_database, 1)
        self.assertIsNone(TaskTestUtils.first(uuid=task_to_delete.uuid))


class UpdateTaskTestCase(TestCase):
    TEST_UUID = "ed7358e8-9c1c-4457-b0af-ee652c9c8cf9"

    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = User.objects.create(username="homerjay@example.com")
        cls.task = TaskTestUtils.create(title="My task", owner_id=cls.user.id)

    def test_task_uuid_is_required(self):
        with self.assertRaisesMessage(AssertionError, "Task uuid is required."):
            update_task(task_uuid="", owner_id=1, task_data={})

    def test_owner_id_is_required(self):
        with self.assertRaisesMessage(AssertionError, "Owner id is required."):
            update_task(task_uuid=self.TEST_UUID, owner_id="", task_data={})

    def test_non_editable_fields_raises_field_error(self):
        updated_data = {
            "title": "Mi updated title",
            "description": "Mi updated description",
            "status": "completed",
            "uuid": self.TEST_UUID,
        }

        with self.assertRaisesMessage(FieldError, "Some fields cannot be updated."):
            update_task(task_uuid=self.task.uuid, owner_id=self.user.id, **updated_data)

    def test_only_task_owner_can_update_task(self):
        no_owned_task = TaskTestUtils.create(title="No owned task")
        updated_data = {
            "title": "Mi updated title",
            "description": "Mi updated description",
            "status": "completed",
        }
        with self.assertRaisesMessage(PermissionError, "User is not task owner"):
            update_task(
                task_uuid=no_owned_task.uuid, owner_id=self.user.id, **updated_data
            )

    def test_invalid_status_raises_exception(self):
        updated_data = {
            "title": "Mi updated title",
            "description": "Mi updated description",
            "status": "myinvalidstatus",
        }

        with self.assertRaises(ValidationError):
            update_task(task_uuid=self.task.uuid, owner_id=self.user.id, **updated_data)

    def test_update_task(self):
        updated_data = {
            "title": "Mi updated title",
            "description": "Mi updated description",
            "status": "completed",
        }

        update_task(task_uuid=self.task.uuid, owner_id=self.user.id, **updated_data)
        self.assertIsNotNone(
            TaskTestUtils.first(
                uuid=self.task.uuid, owner_id=self.user.id, **updated_data
            )
        )


class CreateTasksTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = User.objects.create(username="homerjay@example.com")

    def test_owner_id_is_required(self):
        with self.assertRaisesMessage(AssertionError, "Owner id is required."):
            create_task(owner_id="", task_data={})

    def test_invalid_status_raises_validation_error(self):
        expires_date = timezone.datetime(2099, 12, 31, 23, 59, 59)
        task_data = {
            "title": "My Task",
            "description": "Mi task description",
            "expires": timezone.make_aware(
                expires_date, timezone.get_current_timezone()
            ),
            "status": "myfakestatusnotvalidatall",
        }
        with self.assertRaises(ValidationError):
            create_task(owner_id=self.user.id, **task_data)

    def test_create_task(self):
        expires_date = timezone.datetime(2099, 12, 31, 23, 59, 59)
        task_data = {
            "title": "My Task",
            "description": "Mi task description",
            "expires": timezone.make_aware(
                expires_date, timezone.get_current_timezone()
            ),
            "status": "pending",
        }

        create_task(owner_id=self.user.id, **task_data)
        self.assertIsNotNone(TaskTestUtils.first(owner_id=self.user.id, **task_data), 1)


class ListTasksForUserTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = User.objects.create(username="homerjay@example.com")

    def test_service_returns_queryset(self):
        tasks = list_tasks_for_user(id=self.user.id)
        self.assertIs(type(tasks), QuerySet)

    def test_owner_id_is_required(self):
        with self.assertRaisesMessage(AssertionError, "User id is required."):
            list_tasks_for_user(id="")

    def test_service_list_user_tasks_only(self):
        another_user = User.objects.create(username="nedflanders@example.com")
        TaskTestUtils.create(id=1, title="No listable task", owner_id=another_user.id)
        TaskTestUtils.create(id=2, title="Homer task1", owner_id=self.user.id)
        TaskTestUtils.create(id=3, title="Homer task2", owner_id=self.user.id)

        expected_tasks_ids_for_user = [2, 3]

        tasks = list_tasks_for_user(id=self.user.id)
        retrieved_tasks_ids_for_user = list(tasks.values_list("id", flat=True))
        self.assertListEqual(expected_tasks_ids_for_user, retrieved_tasks_ids_for_user)

        expected_tasks_ids_for_another_user = [1]

        tasks = list_tasks_for_user(id=another_user.id)
        retrieved_tasks_ids_for_another_user = list(tasks.values_list("id", flat=True))
        self.assertListEqual(
            expected_tasks_ids_for_another_user, retrieved_tasks_ids_for_another_user
        )
