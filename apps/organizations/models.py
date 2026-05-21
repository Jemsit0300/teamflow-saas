from django.db import models
from django.conf import settings
from apps.core.models import BaseModel

class Organization(BaseModel):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='owned_organizations'
    )
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class Membership(BaseModel):
    class Role(models.TextChoices):
        ADMIN = 'admin', 'Admin'
        MEMBER = 'member', 'Member'
        VIEWER = 'viewer', 'Viewer'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='memberships'
    )
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name='memberships'
    )
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.MEMBER)

    class Meta(BaseModel.Meta):
        unique_together = ('user', 'organization')

    def __str__(self):
        return f"{self.user} - {self.organization} ({self.role})"
