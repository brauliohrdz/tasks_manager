from django.urls import path
from frontend.tasks.views.tasks_views import CreateTask, TasksList, UpdateTask

urlpatterns = [
    path("", TasksList.as_view(), name="tasks_list"),
    path("create/", CreateTask.as_view(), name="tasks_create"),
    path("update/<uuid:task_uuid>/", UpdateTask.as_view(), name="tasks_update"),
]
