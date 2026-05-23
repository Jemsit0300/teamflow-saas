from rest_framework import serializers
from django.db import transaction
from apps.organizations.models import Organization, Membership
from django.contrib.auth import get_user_model

class OrganizationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ['id', 'name', 'slug']
        read_only_fields = ['id', 'slug']

    def create(self, validated_data):
        user = self.context['request'].user

        with transaction.atomic():
            organization = Organization.objects.create(
                owner=user,
                **validated_data
            )
            Membership.objects.create(
                user=user,
                organization=organization,
                role=Membership.Role.OWNER
            )

        return organization

class OrganizationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ['id', 'name', 'slug', 'created_at']


User = get_user_model()

class InviteMemberSerializer(serializers.Serializer):
    email = serializers.EmailField()
    role = serializers.ChoiceField(choices=Membership.Role.choices)

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Bu email ile kayıtlı kullanıcı bulunamadı.")
        return value

    def validate(self, attrs):
        organization = self.context['organization']
        user = User.objects.get(email=attrs['email'])
        if Membership.objects.filter(user=user, organization=organization).exists():
            raise serializers.ValidationError("Bu kullanıcı zaten bu organizasyonda.")
        return attrs

    def create(self, validated_data):
        organization = self.context['organization']
        user = User.objects.get(email=validated_data['email'])
        return Membership.objects.create(
            user=user,
            organization=organization,
            role=validated_data['role']
        )