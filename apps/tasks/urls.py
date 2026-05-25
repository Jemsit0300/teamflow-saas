from django.urls import path
from apps.tasks.views import TaskListCreateView, TaskDetailView, TaskMoveView

urlpatterns = [
    path('', TaskListCreateView.as_view(), name='task-list-create'),
    path('<uuid:pk>/assign/', TaskDetailView.as_view(), name='task-assign'),
    path('<uuid:pk>/move/', TaskMoveView.as_view(), name='task-move'),
]