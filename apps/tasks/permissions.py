from rest_framework.permissions import BasePermission, SAFE_METHODS
from apps.organizations.models import Membership
from apps.core.utils import get_current_org


class TaskPermission(BasePermission):
    message = "You do not have permission to perform this action."

    def has_permission(self, request, view):
        org = get_current_org(request)
        if not org:
            return False

        return Membership.objects.filter(
            user=request.user,
            organization=org
        ).exists()

    def has_object_permission(self, request, view, obj):
        org = get_current_org(request)
        if not org:
            return False

        membership = Membership.objects.filter(
            user=request.user,
            organization=org
        ).first()

        if not membership:
            return False


        if membership.role in [Membership.Role.OWNER, Membership.Role.ADMIN]:
            return True

        if request.method in SAFE_METHODS:
            return True

        return obj.created_by == request.user