from backend.tasks.services import create_task, list_tasks_for_user, update_task
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.models import QuerySet
from django.test import TestCase
from django.utils import timezone

from .utils import TaskTestUtils


class UpdateTaskTestCase(TestCase):
    TEST_UUID = "ed7358e8-9c1c-4457-b0af-ee652c9c8cf9"

    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = User.objects.create(username="homerjay@example.com")

    def test_task_uuid_is_required(self):
        with self.assertRaisesMessage(AssertionError, "Task uuid is required."):
            update_task(task_uuid="", owner_id=1, task_data={})

    def test_owner_id_is_required(self):
        with self.assertRaisesMessage(AssertionError, "Owner id is required."):
            update_task(task_uuid=self.TEST_UUID, owner_id="", task_data={})

    def test_only_task_owner_can_update_task(self):
        TaskTestUtils.create(uuid=self.TEST_UUID, title="no owned task")
        updated_data = {
            "title": "Mi updated title",
            "description": "Mi updated description",
            "status": "completed",
        }
        with self.assertRaisesMessage(PermissionError, "User is not task owner"):
            update_task(task_uuid=self.TEST_UUID, owner_id=self.user.id, **updated_data)

    def test_invalid_status_raises_exception(self):
        TaskTestUtils.create(
            uuid=self.TEST_UUID, title="My task", owner_id=self.user.id
        )
        updated_data = {
            "title": "Mi updated title",
            "description": "Mi updated description",
            "status": "myinvalidstatus",
        }

        with self.assertRaises(ValidationError):
            update_task(task_uuid=self.TEST_UUID, owner_id=self.user.id, **updated_data)

    def test_update_task(self):
        task = TaskTestUtils.create(
            uuid=self.TEST_UUID, title="task", owner_id=self.user.id
        )
        updated_data = {
            "title": "Mi updated title",
            "description": "Mi updated description",
            "status": "completed",
        }

        update_task(task_uuid=task.uuid, owner_id=self.user.id, **updated_data)
        self.assertIsNotNone(
            TaskTestUtils.get(uuid=task.uuid, owner_id=self.user.id, **updated_data)
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
        self.assertIsNotNone(TaskTestUtils.get(owner_id=self.user.id, **task_data), 1)


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
        TaskTestUtils.create(id=1, title="No listable task", owner=another_user)
        TaskTestUtils.create(id=2, title="Homer task1", owner=self.user)
        TaskTestUtils.create(id=3, title="Homer task2", owner=self.user)

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
