from django.conf.urls import include
from django.urls import path

urlpatterns = [
    path("tasks/", include("frontend.tasks.urls")),
    path("", include("frontend.users.urls")),
]
