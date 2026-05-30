from rest_framework import serializers
from apps.core.models import ActivityLog, Notification


class ActivityLogSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)
    user_full_name = serializers.CharField(source='user.full_name', read_only=True)
    log = serializers.SerializerMethodField()

    class Meta:
        model = ActivityLog
        fields = [
            'id', 'action', 'target_type', 'target_id',
            'metadata', 'user_email', 'user_full_name', 'created_at',
            'log'
        ]

    def get_log(self, obj):
        if obj.action == ActivityLog.Action.TASK_MOVED:
            return f"Moved task from {obj.metadata.get('from')} to {obj.metadata.get('to')}"
        return obj.get_action_display()
    
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'title', 'message', 'is_read', 'created_at']
        read_only_fields = ['id', 'title', 'message', 'created_at']