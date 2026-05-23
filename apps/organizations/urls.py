from django.urls import path
from apps.organizations.views import OrganizationCreateView, InviteMemberView

urlpatterns = [
    path('', OrganizationCreateView.as_view(), name='organization-list-create'),
    path('<uuid:pk>/invite/', InviteMemberView.as_view(), name='organization-invite'),
]