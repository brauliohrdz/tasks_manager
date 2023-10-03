from django.urls import path

from .views import CreateTask, DeleteTask, TasksList, UpdateTask

urlpatterns = [
    path("list/", TasksList.as_view(), name="tasks_list"),
    path("create/", CreateTask.as_view(), name="create_task"),
    path("update/<uuid:task_uuid>/", UpdateTask.as_view(), name="update_task"),
    path("delete/<uuid:task_uuid>/", DeleteTask.as_view(), name="delete_task"),
]
