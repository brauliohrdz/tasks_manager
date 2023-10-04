from django.urls import path

from .views import AuthTokenView

urlpatterns = [
    path("token/", AuthTokenView.as_view(), name="token"),
]
