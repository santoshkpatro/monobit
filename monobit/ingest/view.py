from functools import lru_cache
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.utils import timezone

from monobit.ingest.serializers import IngestSerializer
from monobit.models.project import Project
from monobit.models.job import Job


class IngestAPIView(APIView):
    @lru_cache(maxsize=2048)
    def get_project_by_ingest_key(self, ingest_key):
        return Project.objects.filter(ingest_key=ingest_key).first()

    def post(self, request, *args, **kwargs):
        ingest_key = request.headers.get("X-MONOBIT-KEY")

        if not ingest_key:
            return Response(
                {"error": "Missing X-MONOBIT-KEY header", "status": "fail"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        project = self.get_project_by_ingest_key(ingest_key)
        if not project:
            return Response(
                {"error": "Invalid Project INGEST Key", "status": "fail"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = IngestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        payload = {
            "project_id": str(project.id),
            "ingested_at": timezone.now().isoformat(),
            "data": serializer.data,
        }

        print("Payload", payload)
        Job.objects.create(payload=payload)
        return Response(data={"status": "ok", "error": None}, status=status.HTTP_200_OK)
