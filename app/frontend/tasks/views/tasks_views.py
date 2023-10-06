from backend.tasks.models import Task
from backend.tasks.services import (
    create_task,
    get_task_for_owner,
    list_tasks_for_user,
    update_task,
)
from django import forms
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.forms.models import model_to_dict
from django.http import (
    HttpResponseForbidden,
    HttpResponseNotFound,
    HttpResponseRedirect,
)
from django.shortcuts import render
from django.urls import reverse
from django.views import View


class TaskForm(forms.Form):
    title = forms.CharField(max_length=200)
    description = forms.CharField(widget=forms.Textarea, required=False)
    status = forms.ChoiceField(
        choices=Task.StatusChoices.choices,
        required=False,
        initial=Task.StatusChoices.PENDING,
    )
    expires = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
        required=False,
    )


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


class UpdateTask(LoginRequiredMixin, View):
    template_name = "task_form.html"

    def get(self, request, task_uuid):
        try:
            task = get_task_for_owner(task_uuid, owner_id=request.user.id)
            form = TaskForm(model_to_dict(task))
            return render(request, self.template_name, {"form": form})
        except ObjectDoesNotExist:
            return HttpResponseNotFound("No se ha encontrado la tarea indicada")
        except PermissionError:
            return HttpResponseForbidden("No tiene permisos para realizar esta acción")

    def post(self, request, task_uuid):
        try:
            form = TaskForm(request.POST)
            if form.is_valid():
                update_task(
                    task_uuid=task_uuid, owner_id=request.user.id, **form.cleaned_data
                )
                messages.success(request, "La tarea se ha creado correctamente")
                return HttpResponseRedirect(reverse("tasks_list"))
            return render(request, self.template_name, {"form": form})
        except ObjectDoesNotExist:
            return HttpResponseNotFound("No se ha encontrado la tarea indicada")
        except PermissionError:
            return HttpResponseForbidden("No tiene permisos para realizar esta acción")
