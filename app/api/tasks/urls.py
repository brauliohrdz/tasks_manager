from django.urls import path

from .views import TasksList

urlpatterns = [
    path("list/", TasksList.as_view(), name="tasks_list"),
]
