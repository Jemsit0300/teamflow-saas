from django.db import models
from django.conf import settings
from apps.core.models import BaseModel
from apps.organizations.models import Organization


class Project(BaseModel):
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name='projects'
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name