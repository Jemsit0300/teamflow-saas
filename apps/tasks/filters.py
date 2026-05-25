import django_filters
from apps.tasks.models import Task


class TaskFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(choices=Task.Status.choices)
    priority = django_filters.ChoiceFilter(choices=Task.Priority.choices)
    assignee = django_filters.UUIDFilter(field_name='assignee__id')

    class Meta:
        model = Task
        fields = ['status', 'priority', 'assignee']