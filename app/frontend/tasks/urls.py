from django.urls import path
from frontend.tasks.views.tasks_views import TasksList

urlpatterns = [
    # path("tasks/", include("frontend.tasks.urls")),
    path("", TasksList.as_view(), name="tasks_list"),
]
