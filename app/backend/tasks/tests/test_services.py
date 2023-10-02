from backend.tasks.services import create_task, list_tasks_for_user
from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.test import TestCase
from django.utils import timezone

from .utils import TaskTestUtils


class CreateTasksTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = User.objects.create(username="homerjay@example.com")

    def test_owner_id_is_required(self):
        with self.assertRaisesMessage(AssertionError, "User id is required"):
            create_task(owner_id="", task_data={})

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
        with self.assertRaises(AssertionError):
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
