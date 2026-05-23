from rest_framework.permissions import BasePermission
from apps.organizations.models import Membership


class IsOrgAdminOrOwner(BasePermission):
    message = "You need to be an OWNER or ADMIN to do this."

    def has_permission(self, request, view):
        org_id = view.kwargs.get('pk')
        return Membership.objects.filter(
            user=request.user,
            organization_id=org_id,
            role__in=[Membership.Role.OWNER, Membership.Role.ADMIN]
        ).exists()