from backend.tasks.services import list_tasks_for_user
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View


class TasksList(LoginRequiredMixin, View):
    template_name = "tasks_list.html"

    def get(self, request):
        tasks = list_tasks_for_user(id=request.user.id)
        return render(request, self.template_name, {"tasks": tasks})
