from rest_framework import serializers

from monobit.models.project import Project


class ProjectListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["id", "name", "description", "application_url", "platform", "status"]


class ProjectCreateSerializer(serializers.Serializer):
    name = serializers.CharField()
    description = serializers.CharField(
        required=False, allow_null=True, allow_blank=True
    )
    application_url = serializers.URLField(required=False, allow_null=True)


class ProjectDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            "id",
            "name",
            "description",
            "application_url",
            "ingest_key",
            "platform",
            "status",
            "created_at",
        ]
