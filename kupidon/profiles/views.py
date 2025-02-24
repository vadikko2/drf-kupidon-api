from django.contrib.gis import geos
from django.db import transaction
from drf_spectacular import utils
from rest_framework import authentication, permissions, response, status, views

from profiles import models, serializers


class ProfileView(views.APIView):
    authentication_classes = [authentication.SessionAuthentication, authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @utils.extend_schema(
        tags=["Профили"],
        description="Получение краткой информации о профиле",
        parameters=[
            utils.OpenApiParameter("username", type=str, description="Логин пользователя", required=True),
        ],
        responses={
            status.HTTP_200_OK: serializers.GetBriefProfileSerializer,
            status.HTTP_404_NOT_FOUND: {"detail": "Profile not found."}
        },
    )
    def get(self, request, *args, **kwargs):
        username = request.GET.get('username')
        current_user = request.user.username

        if not username:
            return response.Response(
                {"detail": "Username parameter is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        profile = models.Profile.objects.filter(
            user__username=username,
            user__is_active=True,
            user__is_staff=False,
            user__is_superuser=False,
        ).first()

        if not profile:
            return response.Response({"detail": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)

        current_user_profile = models.Profile.objects.filter(user__username=current_user).first()

        distance_in_km = None
        if current_user_profile and current_user_profile.last_location and profile.last_location:
            user_location = geos.Point(
                current_user_profile.last_location.y,
                current_user_profile.last_location.x,
                srid=4326,
            )
            target_location = geos.Point(
                profile.last_location.y,
                profile.last_location.x,
                srid=4326,
            )
            distance_in_km = user_location.distance(target_location) * 100

        serializer = serializers.GetBriefProfileSerializer(profile, context={'distance_km': distance_in_km})
        return response.Response(serializer.data)

    @utils.extend_schema(
        tags=["Профили"],
        description="Обновление данных профиля",
        request=serializers.PutProfileSerializer,
        responses={
            status.HTTP_200_OK: serializers.PutProfileSerializer,
            status.HTTP_201_CREATED: serializers.PutProfileSerializer,
        },
    )
    def put(self, request, *args, **kwargs):
        with transaction.atomic():
            user = request.user
            data = request.data.copy()

            try:
                profile = models.Profile.objects.get(user=user)
                created = False
                status_code = status.HTTP_200_OK
            except models.Profile.DoesNotExist:
                profile = None
                created = True
                status_code = status.HTTP_201_CREATED

            serializer = serializers.PutProfileSerializer(
                instance=profile,
                data=data,
                context={'request': request},
                partial=not created
            )

            serializer.is_valid(raise_exception=True)
            serializer.save(user=user)

            return response.Response(
                serializers.PutProfileSerializer(
                    serializer.instance,
                    context={'request': request}
                ).data,
                status=status_code
            )
