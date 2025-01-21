from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import authentication, permissions, views
from rest_framework.response import Response

from profiles import models
from profiles.serializers import brief_profile


@extend_schema(
    parameters=[
        OpenApiParameter("username", type=str, description="Логин пользователя", required=True),
    ],
    responses={200: brief_profile.BriefProfileSerializer},
)
class BriefProfileView(views.APIView):
    serializer_class = brief_profile.BriefProfileSerializer
    authentication_classes = [authentication.SessionAuthentication, authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        login = request.GET.get('username')
        if not login:
            return Response({"detail": "Login parameter is required."}, status=400)

        # Получение объекта из базы данных
        profile = models.Profile.objects.filter(user__username=login).first()
        if not profile:
            return Response({"detail": "Profile not found."}, status=404)

        serializer = self.serializer_class(profile)
        return Response(serializer.data)
