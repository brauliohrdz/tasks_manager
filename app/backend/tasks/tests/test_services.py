from backend.tasks.models import Task
from backend.tasks.services import list_tasks_for_user
from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.test import TestCase


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
        Task.objects.create(id=1, title="No listable task", owner=another_user)
        Task.objects.create(id=2, title="Homer task1", owner=self.user)
        Task.objects.create(id=3, title="Homer task2", owner=self.user)

        expected_tasks_ids = [2, 3]

        tasks = list_tasks_for_user(id=self.user.id)
        retrieved_tasks_ids = list(tasks.values_list("id", flat=True))
        self.assertListEqual(expected_tasks_ids, retrieved_tasks_ids)
