from django.conf.urls import include
from django.urls import path

urlpatterns = [
    path("tasks/", include("api.tasks.urls")),
    path("auth/", include("api.auth.urls")),
]
