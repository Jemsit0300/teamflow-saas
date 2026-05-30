from django.urls import path
from apps.organizations.views import OrganizationCreateView, InviteMemberView, ActivityLogView

urlpatterns = [
    path('', OrganizationCreateView.as_view(), name='organization-list-create'),
    path('<uuid:pk>/invite/', InviteMemberView.as_view(), name='organization-invite'),
    path('<uuid:pk>/activity/', ActivityLogView.as_view(), name='organization-activity'),
]