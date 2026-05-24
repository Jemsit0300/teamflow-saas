from rest_framework.permissions import BasePermission, SAFE_METHODS
from apps.organizations.models import Membership
from apps.core.utils import get_current_org


class IsOrgAdminOrReadOnly(BasePermission):
    message = "You must be an OWNER or ADMIN to perform this action."

    def has_permission(self, request, view):
        org = get_current_org(request)
        if not org:
            return False

        if request.method in SAFE_METHODS:
            return Membership.objects.filter(
                user=request.user,
                organization=org
            ).exists()

        return Membership.objects.filter(
            user=request.user,
            organization=org,
            role__in=[Membership.Role.OWNER, Membership.Role.ADMIN]
        ).exists()