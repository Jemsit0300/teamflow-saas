from rest_framework import serializers
from .models import Project

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'status', 'created_at']
        read_only_fields = ['id', 'created_at']

class ProjectCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['name', 'description']

    def create(self, validated_data):
        organization = self.context['organization']
        return Project.objects.create(organization=organization, **validated_data)