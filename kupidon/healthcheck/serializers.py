import enum

from rest_framework import serializers


class HealthStatus(enum.StrEnum):
    healthy = "healthy"
    unhealthy = "unhealthy"


class CheckSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=HealthStatus)
    message = serializers.CharField(allow_blank=True)


class HealthCheckSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=HealthStatus)
    checks = serializers.DictField(
        child=CheckSerializer()
    )
