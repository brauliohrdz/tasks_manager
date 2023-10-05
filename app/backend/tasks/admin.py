from backend.tasks.models import Task, TaskImage
from django.contrib import admin


class BaseModelAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        return self.readonly_fields if obj else []

    def get_exclude(delf, request, obj=None):
        return []


class TaskAdmin(BaseModelAdmin):
    list_display = ("uuid", "title", "owner", "status", "created")
    fields = ("title", "description", "owner", "status", "expires")

    def owner(self, obj):
        return obj.owner.username


admin.site.register(Task, TaskAdmin)


class TaskImageAdmin(admin.ModelAdmin):
    list_display = ("uuid", "image", "task")

    def task(self, obj):
        return obj.task.title


admin.site.register(TaskImage, TaskImageAdmin)
