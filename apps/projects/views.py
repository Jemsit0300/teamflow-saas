from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from apps.projects.models import Project
from apps.projects.serializers import ProjectSerializer, ProjectCreateSerializer
from apps.core.utils import get_current_org
from apps.projects.permissions import IsOrgAdminOrReadOnly


class ProjectListCreateView(APIView):
    permission_classes = [IsAuthenticated, IsOrgAdminOrReadOnly]

    def get(self, request):
        org = get_current_org(request)
        if not org:
            return Response({"error": "X-Organization-ID header is required."}, status=status.HTTP_400_BAD_REQUEST)

        projects = Project.objects.filter(organization=org)

        status_param = request.query_params.get('status')
        if status_param:
            projects = projects.filter(status=status_param)

        ordering = request.query_params.get('ordering', '-created_at')
        projects = projects.order_by(ordering)

        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    def post(self, request):
        org = get_current_org(request)
        if not org:
            return Response({"error": "X-Organization-ID header is required."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ProjectCreateSerializer(
            data=request.data,
            context={'organization': org}
        )
        if serializer.is_valid():
            project = serializer.save()
            return Response(ProjectSerializer(project).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectDetailView(APIView):
    permission_classes = [IsAuthenticated, IsOrgAdminOrReadOnly]

    def get_object(self, slug, org):
        try:
            return Project.objects.get(slug=slug, organization=org)
        except Project.DoesNotExist:
            return None

    def get(self, request, slug):
        org = get_current_org(request)
        if not org:
            return Response({"error": "X-Organization-ID header is required."}, status=status.HTTP_400_BAD_REQUEST)

        project = self.get_object(slug, org)
        if not project:
            return Response({"error": "Project not found."}, status=status.HTTP_404_NOT_FOUND)

        return Response(ProjectSerializer(project).data)

    def patch(self, request, slug):
        org = get_current_org(request)
        if not org:
            return Response({"error": "X-Organization-ID header is required."}, status=status.HTTP_400_BAD_REQUEST)

        project = self.get_object(slug, org)
        if not project:
            return Response({"error": "Project not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProjectSerializer(project, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, slug):
        org = get_current_org(request)
        if not org:
            return Response({"error": "X-Organization-ID header is required."}, status=status.HTTP_400_BAD_REQUEST)

        project = self.get_object(slug, org)
        if not project:
            return Response({"error": "Project not found."}, status=status.HTTP_404_NOT_FOUND)

        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)