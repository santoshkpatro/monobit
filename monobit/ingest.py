from rest_framework.views import APIView
from rest_framework import serializers, status
from rest_framework.response import Response


class IngestSerializer(serializers.Serializer):
    timestamp = serializers.DateTimeField()
    message = serializers.CharField()
    stacktrace = serializers.JSONField()


class IngestAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = IngestSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        print("Validated Data: ", validated_data)
        return Response(data=None, status=status.HTTP_200_OK)
