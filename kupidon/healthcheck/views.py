import enum
import typing

from django.db import connection
from rest_framework import response, status, views


class HealthStatus(enum.StrEnum):
    healthy = "healthy"
    unhealthy = "unhealthy"


Message: typing.TypeAlias = str


class HealthCheckView(views.APIView):
    def get(self, request):

        checks_mapping = {
            "database": self.check_database,
            # остальные проверки
        }

        common_status = HealthStatus.healthy
        checks = {}
        for check_name, check in checks_mapping.items():
            check_status, message = check()
            checks[check_name] = {
                "status": check_status,
                "message": message,
            }
            if check_status == HealthStatus.unhealthy:
                common_status = HealthStatus.unhealthy

        response_status = status.HTTP_200_OK if (
                common_status == HealthStatus.healthy) else status.HTTP_503_SERVICE_UNAVAILABLE

        return response.Response({
            "status": common_status,
            "checks": checks
        }, status=response_status)

    @staticmethod
    def check_database() -> tuple[HealthStatus, Message]:
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
            return HealthStatus.healthy, ""
        except Exception as e:
            return HealthStatus.unhealthy, str(e)
