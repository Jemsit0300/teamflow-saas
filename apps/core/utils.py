from apps.organizations.models import Organization, Membership


def get_current_org(request):
    org_id = request.headers.get('X-Organization-ID')

    if not org_id:
        return None

    try:
        organization = Organization.objects.get(id=org_id)
    except Organization.DoesNotExist:
        return None

    is_member = Membership.objects.filter(
        user=request.user,
        organization=organization
    ).exists()

    if not is_member:
        return None

    return organization


def log_activity(user, org, action, target=None, metadata={}):
    from apps.core.models import ActivityLog
    ActivityLog.objects.create(
        user=user,
        organization=org,
        action=action,
        target_type=target.__class__.__name__ if target else '',
        target_id=target.id if target else None,
        metadata=metadata
    )