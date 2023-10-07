from django.urls import include, path
from frontend.tasks.views import (
    CreateTask,
    CreateTaskImage,
    DeleteTask,
    DeleteTaskImage,
    TasksList,
    UpdateTask,
)

images_patterns = [
    path(
        "create/<uuid:task_uuid>/", CreateTaskImage.as_view(), name="tasks_image_create"
    ),
    path(
        "delete/<uuid:task_image_uuid>/",
        DeleteTaskImage.as_view(),
        name="tasks_image_delete",
    ),
]

tasks_patterns = [
    path("create/", CreateTask.as_view(), name="tasks_create"),
    path("update/<uuid:task_uuid>/", UpdateTask.as_view(), name="tasks_update"),
    path("delete/<uuid:task_uuid>/", DeleteTask.as_view(), name="tasks_delete"),
]

urlpatterns = [
    path("", TasksList.as_view(), name="tasks_list"),
    path("tasks/", include(tasks_patterns)),
    path("images/", include(images_patterns)),
]
