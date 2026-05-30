from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from apps.organizations.models import Organization, Membership
from apps.organizations.serializers import (
    OrganizationCreateSerializer,
    OrganizationListSerializer,
    InviteMemberSerializer
)
from apps.organizations.permissions import IsOrgAdminOrOwner
from apps.core.models import ActivityLog
from apps.core.serializers import ActivityLogSerializer

class OrganizationCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        organizations = Organization.objects.filter(
            memberships__user=request.user
        )
        serializer = OrganizationListSerializer(organizations, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = OrganizationCreateSerializer(
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            organization = serializer.save()
            return Response(
                OrganizationCreateSerializer(organization).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class InviteMemberView(APIView):
    permission_classes = [IsAuthenticated, IsOrgAdminOrOwner]

    def post(self, request, pk):
        try:
            organization = Organization.objects.get(pk=pk)
        except Organization.DoesNotExist:
            return Response({"error": "Organization not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = InviteMemberSerializer(
            data=request.data,
            context={'organization': organization}
        )
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User added."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ActivityLogView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            organization = Organization.objects.get(pk=pk)
        except Organization.DoesNotExist:
            return Response({"error": "Organization not found."}, status=status.HTTP_404_NOT_FOUND)

        is_member = Membership.objects.filter(
            user=request.user,
            organization=organization
        ).exists()
        if not is_member:
            return Response({"error": "You are not a member of this organization."}, status=status.HTTP_403_FORBIDDEN)

        logs = ActivityLog.objects.filter(
            organization=organization
        ).select_related('user').order_by('-created_at')[:50]

        serializer = ActivityLogSerializer(logs, many=True)
        return Response(serializer.data)