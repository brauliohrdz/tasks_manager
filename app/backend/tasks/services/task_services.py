from typing import Optional

from backend.tasks.models import Task
from django.db.models import QuerySet

from .filters import TasksListFilter


def get_task_for_owner(task_uuid: str, owner_id: int):
    task = Task.objects.get(uuid=task_uuid)
    is_task_owner = task.owner_id == owner_id
    if is_task_owner:
        return task
    raise PermissionError("User is not task owner.")


def list_tasks_for_user(id: int, query_params: Optional[dict] = None) -> QuerySet[Task]:
    assert id, "User id is required."
    tasks = Task.objects.filter(owner_id=id).order_by("-created")
    if query_params:
        tasks = TasksListFilter(query_params, tasks).qs
    return tasks


def create_task(owner_id: int, **kwargs) -> Task:
    assert owner_id, "Owner id is required."
    task = Task(owner_id=owner_id, **kwargs)
    task.full_clean()
    task.save()
    return task


def update_task(task_uuid: int, owner_id: int, **kwargs) -> None:
    assert task_uuid, "Task uuid is required."
    assert owner_id, "Owner id is required."

    fields_to_update = list(kwargs.keys())
    task = get_task_for_owner(task_uuid=task_uuid, owner_id=owner_id)
    task.validate_fields_are_editable(fields_to_update)
    task.set_fields(**kwargs)
    task.full_clean()
    task.save(update_fields=fields_to_update)


def delete_task(task_uuid: int, owner_id: int, **kwargs) -> None:
    assert task_uuid, "Task uuid is required."
    assert owner_id, "Owner id is required."

    task = get_task_for_owner(task_uuid=task_uuid, owner_id=owner_id)
    task.delete()
