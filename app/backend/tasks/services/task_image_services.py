from backend.tasks.models import TaskImage

from .task_services import get_task_for_owner


def get_task_image_for_owner(task_image_uuid: str, owner_id: int) -> TaskImage:
    assert task_image_uuid, "TaskImage uuid is required."
    assert owner_id, "Owner id is required."
    task_image = TaskImage.objects.get(uuid=task_image_uuid)
    is_task_image_owner = task_image.owner_id == owner_id
    if is_task_image_owner:
        return task_image
    raise PermissionError("User is not image owner.")


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
