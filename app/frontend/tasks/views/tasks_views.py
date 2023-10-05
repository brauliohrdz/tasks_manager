from backend.tasks.models import Task
from backend.tasks.services import create_task, list_tasks_for_user
from django import forms
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View


class TaskForm(forms.Form):
    title = forms.CharField(max_length=200)
    description = forms.CharField(widget=forms.Textarea)
    status = forms.ChoiceField(choices=Task.StatusChoices.choices)
    expires = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))


class TasksList(LoginRequiredMixin, View):
    template_name = "tasks_list.html"

    def get(self, request):
        tasks = list_tasks_for_user(id=request.user.id)
        return render(request, self.template_name, {"tasks": tasks})


class CreateTask(LoginRequiredMixin, View):
    template_name = "task_form.html"

    def get(self, request):
        form = TaskForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = TaskForm(request.POST)
        if form.is_valid():
            create_task(owner_id=request.user.id, **form.cleaned_data)
            messages.success(request, "La tarea se ha creado correctamente")
            return HttpResponseRedirect(reverse("tasks_list"))
        return render(
            request,
            self.template_name,
            {"form": form},
        )
