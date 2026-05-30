from django.urls import path
from apps.tasks.views import TaskListCreateView, TaskDetailView, TaskMoveView, CommentListCreateView, CommentDetailView

urlpatterns = [
    path('', TaskListCreateView.as_view(), name='task-list-create'),
    path('<uuid:pk>/assign/', TaskDetailView.as_view(), name='task-assign'),
    path('<uuid:pk>/move/', TaskMoveView.as_view(), name='task-move'),
    path('<uuid:pk>/comments/', CommentListCreateView.as_view(), name='comment-list-create'),
    path('comments/<uuid:pk>/', CommentDetailView.as_view(), name='comment-detail'),
]