from backend.tasks.models import Task, TaskImage
from django.core.exceptions import FieldError
from django.db.models import QuerySet


def get_task_for_owner(task_uuid: str, owner_id: int):
    task = Task.objects.get(uuid=task_uuid)
    is_task_owner = task.owner_id == owner_id
    if is_task_owner:
        return task
    raise PermissionError("User is not task owner.")


def get_task_image_for_owner(task_image_uuid: str, owner_id: int) -> TaskImage:
    assert task_image_uuid, "TaskImage uuid is required."
    assert owner_id, "Owner id is required."
    task_image = TaskImage.objects.get(uuid=task_image_uuid)
    is_task_image_owner = task_image.owner_id == owner_id
    if is_task_image_owner:
        return task_image
    raise PermissionError("User is not image owner.")


def list_tasks_for_user(id: int) -> QuerySet[Task]:
    assert id, "User id is required."
    return Task.objects.filter(owner_id=id).prefetch_related("images")


def create_task(owner_id: int, **kwargs) -> Task:
    assert owner_id, "Owner id is required."
    task = Task(owner_id=owner_id, **kwargs)
    task.full_clean()
    task.save()
    return task


def update_task(task_uuid: int, owner_id: int, **kwargs) -> None:
    assert task_uuid, "Task uuid is required."
    assert owner_id, "Owner id is required."

    task = get_task_for_owner(task_uuid=task_uuid, owner_id=owner_id)
    editable_fields = Task.editable_fields()
    all_fields_are_editable = all([field in editable_fields for field in kwargs.keys()])
    if not all_fields_are_editable:
        raise FieldError("Some fields cannot be updated.")

    updated_fields = []
    for field, value in kwargs.items():
        if field in Task.editable_fields():
            setattr(task, field, value)
            updated_fields.append(field)

    task.full_clean()
    task.save(update_fields=updated_fields)


def delete_task(task_uuid: int, owner_id: int, **kwargs) -> None:
    assert task_uuid, "Task uuid is required."
    assert owner_id, "Owner id is required."

    task = get_task_for_owner(task_uuid=task_uuid, owner_id=owner_id)
    task.delete()


def create_task_image(task_uuid: int, owner_id: int, image) -> None:
    assert task_uuid, "Task uuid is required."
    assert owner_id, "Owner id is required."

    task = get_task_for_owner(task_uuid=task_uuid, owner_id=owner_id)
    task_image = TaskImage(image=image, task_id=task.id)
    task_image.full_clean()
    task_image.save()
    return task_image


def delete_task_image(task_image_uuid: int, owner_id: int) -> None:
    assert task_image_uuid, "TaskImage uuid is required."
    assert owner_id, "Owner id is required."

    task_image = get_task_image_for_owner(task_image_uuid, owner_id)
    task_image.delete()
