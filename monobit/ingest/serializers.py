from rest_framework import serializers


class CodeContextSerializer(serializers.Serializer):
    lineno = serializers.IntegerField()
    content = serializers.CharField(allow_blank=True)
    is_exception_line = serializers.BooleanField()


class FrameSerializer(serializers.Serializer):
    filename = serializers.CharField()
    function = serializers.CharField()
    lineno = serializers.IntegerField()
    code_context = CodeContextSerializer(many=True)


class ExceptionSerializer(serializers.Serializer):
    type = serializers.CharField()
    message = serializers.CharField(allow_blank=True)
    frames = FrameSerializer(many=True)


class SDKSerializer(serializers.Serializer):
    name = serializers.CharField()
    version = serializers.CharField()


class RuntimeSerializer(serializers.Serializer):
    name = serializers.CharField()
    version = serializers.CharField()


class SystemSerializer(serializers.Serializer):
    os = serializers.CharField()
    os_version = serializers.CharField()
    architecture = serializers.CharField()
    hostname = serializers.CharField()


class ProcessSerializer(serializers.Serializer):
    pid = serializers.IntegerField()
    thread = serializers.CharField()


class ServiceSerializer(serializers.Serializer):
    name = serializers.CharField(required=False)
    version = serializers.CharField(required=False)


class IngestSerializer(serializers.Serializer):
    occurrence_id = serializers.CharField()
    timestamp = serializers.DateTimeField()

    sdk = SDKSerializer()
    environment = serializers.CharField()

    service = ServiceSerializer(required=False)
    runtime = RuntimeSerializer()
    system = SystemSerializer()
    process = ProcessSerializer()

    exception = ExceptionSerializer()
