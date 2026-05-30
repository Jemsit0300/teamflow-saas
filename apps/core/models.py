import uuid
from django.db import models
from django.conf import settings

class BaseModel(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class   ActivityLog(BaseModel):
    class Action(models.TextChoices):
        TASK_CREATED = 'TASK_CREATED', 'Task Created'
        TASK_UPDATED = 'TASK_UPDATED', 'Task Updated'
        TASK_MOVED = 'TASK_MOVED', 'Task Moved'
        TASK_ASSIGNED = 'TASK_ASSIGNED', 'Task Assigned'
        COMMENT_CREATED = 'COMMENT_CREATED', 'Comment Created'
        PROJECT_CREATED = 'PROJECT_CREATED', 'Project Created'
        USER_INVITED = 'USER_INVITED', 'User Invited'

    organization = models.ForeignKey(
        'organizations.Organization',
        on_delete=models.CASCADE,
        related_name='activity_logs'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='activity_logs'
    )
    action = models.CharField(max_length=50, choices=Action.choices)
    target_type = models.CharField(max_length=50)
    target_id = models.UUIDField(null=True, blank=True)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user} - {self.action}"

class Notification(BaseModel):
    class Meta:
        ordering = ['-created_at']

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    title = models.CharField(max_length=255)
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} - {self.title}"