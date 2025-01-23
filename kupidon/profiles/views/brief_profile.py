from django.contrib.gis.geos import Point
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
        username = request.GET.get('username')
        current_user = request.user.username

        if not username:
            return Response({"detail": "Login parameter is required."}, status=400)

        profile = models.Profile.objects.filter(
            user__username=username,
            user__is_active=True,
            user__is_staff=False,
            user__is_superuser=False,
        ).first()

        if not profile:
            return Response({"detail": "Profile not found."}, status=404)

        current_user_profile = models.Profile.objects.filter(user__username=current_user).first()

        distance_in_km = None
        if current_user_profile and current_user_profile.last_location and profile.last_location:
            user_location = Point(
                current_user_profile.last_location.y,
                current_user_profile.last_location.x,
                srid=4326,
            )
            target_location = Point(
                profile.last_location.y,
                profile.last_location.x,
                srid=4326,
            )
            distance_in_km = user_location.distance(target_location) * 100

        serializer = self.serializer_class(profile, context={'distance_km': distance_in_km})
        return Response(serializer.data)
