from backend.tasks.models import Task
from django.db.models import QuerySet


def list_tasks_for_user(id: int) -> QuerySet[Task]:
    assert id, "User id is required"
    return Task.objects.filter(owner_id=id)
