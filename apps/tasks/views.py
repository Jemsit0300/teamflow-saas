from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from apps.tasks.models import Task
from apps.tasks.serializers import TaskSerializer, TaskCreateSerializer, AssignTaskSerializer, MoveTaskSerializer
from apps.projects.models import Project
from apps.core.utils import get_current_org
from apps.tasks.filters import TaskFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db import models
from apps.tasks.permissions import TaskPermission


class TaskListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get_project(self, project_slug, org):
        try:
            return Project.objects.get(slug=project_slug, organization=org)
        except Project.DoesNotExist:
            return None

    def get(self, request, project_slug):
        org = get_current_org(request)
        if not org:
            return Response({"error": "X-Organization-ID header is required."}, status=status.HTTP_400_BAD_REQUEST)

        project = self.get_project(project_slug, org)
        if not project:
            return Response({"error": "Project not found."}, status=status.HTTP_404_NOT_FOUND)

        tasks = Task.objects.filter(project=project)

        # filtering
        filterset = TaskFilter(request.query_params, queryset=tasks)
        if filterset.is_valid():
            tasks = filterset.qs

        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

        # search
        search = request.query_params.get('search')
        if search:
            tasks = tasks.filter(
                models.Q(title__icontains=search) |
                models.Q(description__icontains=search)
            )

        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)
    
        # ordering
        ordering = request.query_params.get('ordering', '-created_at')
        allowed_orderings = ['created_at', '-created_at', 'due_date', '-due_date', 'priority', '-priority']
        if ordering in allowed_orderings:
            tasks = tasks.order_by(ordering)

    def post(self, request, project_slug):
        org = get_current_org(request)
        if not org:
            return Response({"error": "X-Organization-ID header is required."}, status=status.HTTP_400_BAD_REQUEST)

        project = self.get_project(project_slug, org)
        if not project:
            return Response({"error": "Project not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = TaskCreateSerializer(
            data=request.data,
            context={
                'project': project,
                'request': request
            }
        )
        if serializer.is_valid():
            task = serializer.save()
            return Response(TaskSerializer(task).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class TaskDetailView(APIView):
    permission_classes = [IsAuthenticated, TaskPermission]

    def patch(self, request, pk):
        org = get_current_org(request)
        if not org:
            return Response({"error": "X-Organization-ID header is required."}, status=status.HTTP_400_BAD_REQUEST)

        task = self.get_object(pk, org)
        if not task:
            return Response({"error": "Task not found."}, status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, task)  # ← obje kontrolü

        serializer = AssignTaskSerializer(
            task,
            data=request.data,
            context={'org': org}
        )
        if serializer.is_valid():
            task = serializer.save()
            return Response(TaskSerializer(task).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskMoveView(APIView):
    permission_classes = [IsAuthenticated, TaskPermission]

    def patch(self, request, pk):
        org = get_current_org(request)
        if not org:
            return Response({"error": "X-Organization-ID header is required."}, status=status.HTTP_400_BAD_REQUEST)

        task = self.get_object(pk, org)
        if not task:
            return Response({"error": "Task not found."}, status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, task)  # ← obje kontrolü

        serializer = MoveTaskSerializer(task, data=request.data)
        if serializer.is_valid():
            task = serializer.save()
            return Response(TaskSerializer(task).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)