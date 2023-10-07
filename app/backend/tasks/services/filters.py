import django_filters as df
from backend.tasks.models import Task


class TasksListFilter(df.FilterSet):
    title = df.CharFilter(lookup_expr="icontains")
    status = df.ChoiceFilter(choices=Task.StatusChoices.choices)
