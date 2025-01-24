import typing

from django.db import connection
from rest_framework import generics, response, status

from healthcheck import serializers

Message: typing.TypeAlias = str


class HealthCheckView(generics.GenericAPIView):
    serializer_class = serializers.HealthCheckSerializer
    permission_classes = []

    def get(self, request):
        checks_mapping = {
            "database": self.check_database,
            # другие проверки...
        }

        common_status = serializers.HealthStatus.healthy
        checks = {}

        for check_name, check in checks_mapping.items():
            check_status, message = check()
            checks[check_name] = {
                "status": check_status,
                "message": message,
            }
            if check_status == serializers.HealthStatus.unhealthy:
                common_status = serializers.HealthStatus.unhealthy

        response_data = {
            "status": common_status,
            "checks": checks
        }

        serializer = self.get_serializer(data=response_data)
        serializer.is_valid(raise_exception=True)  # Проверка структуры ответа
        return response.Response(
            serializer.data,
            status=status.HTTP_200_OK if
            common_status == serializers.HealthStatus.healthy else status.HTTP_503_SERVICE_UNAVAILABLE
        )

    @staticmethod
    def check_database():
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
            return serializers.HealthStatus.healthy, ""
        except Exception as e:
            return serializers.HealthStatus.unhealthy, str(e)
