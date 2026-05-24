from django.urls import path
from apps.projects.views import ProjectListCreateView, ProjectDetailView

urlpatterns = [
    path('', ProjectListCreateView.as_view(), name='project-list-create'),
    path('<slug:slug>/', ProjectDetailView.as_view(), name='project-detail'),
]