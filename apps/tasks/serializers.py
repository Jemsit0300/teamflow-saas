from rest_framework import serializers
from django.contrib.auth import get_user_model
from apps.tasks.models import Task, Comment
from apps.organizations.models import Membership

User = get_user_model()


class AssignTaskSerializer(serializers.Serializer):
    assignee_id = serializers.UUIDField()

    def validate_assignee_id(self, value):
        try:
            user = User.objects.get(id=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("Kullanıcı bulunamadı.")

        # Aynı org'da mı?
        org = self.context['org']
        if not Membership.objects.filter(user=user, organization=org).exists():
            raise serializers.ValidationError("Bu kullanıcı aynı organizasyonda değil.")

        return value

    def update(self, instance, validated_data):
        user = User.objects.get(id=validated_data['assignee_id'])
        instance.assignee = user
        instance.save()
        return instance

class TaskSerializer(serializers.ModelSerializer):
    assignee_email = serializers.EmailField(source='assignee.email', read_only=True)
    created_by_email = serializers.EmailField(source='created_by.email', read_only=True)
    is_overdue = serializers.BooleanField(read_only=True)

    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'status', 'priority',
            'due_date', 'assignee', 'assignee_email',
            'created_by', 'created_by_email',
            'is_overdue', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at']

class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['title', 'description', 'priority', 'due_date', 'assignee']

    def create(self, validated_data):
        project = self.context['project']
        user = self.context['request'].user
        return Task.objects.create(
            project=project,
            created_by=user,
            **validated_data
        )
    
class AssignTaskSerializer(serializers.Serializer):
    assignee_id = serializers.UUIDField()

    def validate_assignee_id(self, value):
        try:
            user = User.objects.get(id=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("Kullanıcı bulunamadı.")

        # Aynı org'da mı?
        org = self.context['org']
        if not Membership.objects.filter(user=user, organization=org).exists():
            raise serializers.ValidationError("Bu kullanıcı aynı organizasyonda değil.")

        return value

    def update(self, instance, validated_data):
        user = User.objects.get(id=validated_data['assignee_id'])
        instance.assignee = user
        instance.save()
        return instance
    
class MoveTaskSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=Task.Status.choices)

    def update(self, instance, validated_data):
        instance.status = validated_data['status']
        instance.save()
        return instance    
    
class CommentSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'content', 'user', 'user_email', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['content']

    def create(self, validated_data):
        task = self.context['task']
        user = self.context['request'].user
        return Comment.objects.create(
            task=task,
            user=user,
            **validated_data
        )