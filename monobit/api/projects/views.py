from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from monobit.models.project import Project
from monobit.api.projects.serializers import (
    ProjectListSerializer,
    ProjectCreateSerializer,
    ProjectDetailSerializer,
)


class ProjectViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        projects = Project.objects.filter(memberships__user=request.user)
        serializer = ProjectListSerializer(projects, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = ProjectCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        new_project = Project.bootstrap(request.user, **serializer.validated_data)
        new_project_serializer = ProjectDetailSerializer(new_project)

        return Response(
            data=new_project_serializer.data, status=status.HTTP_201_CREATED
        )
