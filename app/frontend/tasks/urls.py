from django.urls import path
from frontend.tasks.views.tasks_views import TasksList

urlpatterns = [
    path("", TasksList.as_view(), name="tasks_list"),
]
