from backend.tasks.models import Task
from django.db.models import QuerySet


def list_tasks_for_user(id: int) -> QuerySet[Task]:
    assert id, "User id is required."
    return Task.objects.filter(owner_id=id)


def create_task(owner_id: int, **kwargs) -> None:
    assert owner_id, "Owner id is required."
    task = Task(owner_id=owner_id, **kwargs)
    task.full_clean()
    task.save()


def update_task(task_uuid: int, owner_id: int, **kwargs) -> None:
    assert task_uuid, "Task uuid is required."
    assert owner_id, "Owner id is required."

    task = Task.objects.get(uuid=task_uuid, owner_id=owner_id)
    updated_fields = []
    for field, value in kwargs.items():
        if field in Task.editable_fields():
            setattr(task, field, value)
            updated_fields.append(field)

    task.full_clean()
    task.save(update_fields=updated_fields)
