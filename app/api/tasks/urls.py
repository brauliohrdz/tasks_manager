from django.urls import include, path

from .views import (
    CreateTask,
    CreateTaskImage,
    DeleteTask,
    DeleteTaskImage,
    ListTaskImages,
    TasksList,
    UpdateTask,
)

images_patterns = [
    path(
        "list/<uuid:task_uuid>/",
        ListTaskImages.as_view(),
        name="list_task_images",
    ),
    path(
        "create/<uuid:task_uuid>/",
        CreateTaskImage.as_view(),
        name="create_task_image",
    ),
    path(
        "delete/<uuid:task_image_uuid>/",
        DeleteTaskImage.as_view(),
        name="delete_task_image",
    ),
]


urlpatterns = [
    path("list/", TasksList.as_view(), name="tasks_list"),
    path("create/", CreateTask.as_view(), name="create_task"),
    path("update/<uuid:task_uuid>/", UpdateTask.as_view(), name="update_task"),
    path("delete/<uuid:task_uuid>/", DeleteTask.as_view(), name="delete_task"),
    path("image/", include(images_patterns)),
]
