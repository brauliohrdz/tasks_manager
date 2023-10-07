from django.conf.urls import include
from django.urls import path

urlpatterns = [
    path("", include("frontend.tasks.urls")),
    path("accounts/", include("frontend.users.urls")),
]
