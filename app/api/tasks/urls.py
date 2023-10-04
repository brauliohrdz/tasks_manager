from django.urls import include, path

from .views import (
    CreateTask,
    CreateTaskImage,
    DeleteTask,
    DeleteTaskImage,
    TasksList,
    UpdateTask,
)

images_patterns = [
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
