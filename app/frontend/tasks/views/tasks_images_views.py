from backend.tasks.services import create_task_image
from django import forms
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.http import (
    HttpResponseForbidden,
    HttpResponseNotFound,
    HttpResponseRedirect,
)
from django.urls import reverse
from django.views import View


class TaskImageForm(forms.Form):
    image = forms.ImageField()


class CreateTaskImage(View):
    def post(self, request, task_uuid):
        try:
            form = TaskImageForm(request.POST, request.FILES)
            if form.is_valid():
                create_task_image(
                    task_uuid,
                    owner_id=request.user.id,
                    image=form.cleaned_data.get("image"),
                )
                messages.success(request, "La imagen se ha guardado correctamente")
            else:
                messages.error(request, form.errors)
            return HttpResponseRedirect(reverse("tasks_update", args=[task_uuid]))
        except ObjectDoesNotExist:
            return HttpResponseNotFound("No se ha encontrado la tarea indicada")
        except PermissionError:
            return HttpResponseForbidden("No tiene permisos para realizar esta acción")
