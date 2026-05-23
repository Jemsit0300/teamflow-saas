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