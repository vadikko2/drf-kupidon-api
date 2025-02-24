from django.contrib.auth import models as auth_models
from drf_spectacular import utils
from rest_framework import authentication, generics, permissions, response, status

from images import models, serializers


class ProfileImagesView(generics.GenericAPIView):
    authentication_classes = [authentication.SessionAuthentication, authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @utils.extend_schema(
        description="Получение списка фотографий профиля",
        tags=["Фотографии"],
        parameters=[
            utils.OpenApiParameter("username", type=str, description="Логин пользователя", required=True),
        ],
        responses={status.HTTP_200_OK: serializers.ProfileImagesSerializer},
    )
    def get(self, request, *args, **kwargs):
        username = request.GET.get('username')
        if not username:
            return response.Response(
                {"detail": "Username parameter is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = auth_models.User.objects.filter(
            username=username,
            is_active=True,
            is_staff=False,
            is_superuser=False,
        ).first()

        if not user:
            return response.Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        images_queryset = models.Image.objects.filter(user__username=username).order_by('profile_order', '-id')

        images_data = [
            {
                'order': image.profile_order,
                'url': image.url,
            }
            for image in images_queryset
        ]

        serializer = serializers.ProfileImagesSerializer(data={
            'username': username,
            'images': images_data,
        })

        if serializer.is_valid():
            return response.Response(serializer.data)
        else:
            return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @utils.extend_schema(
        description="Загрузка фотографий профиля",
        tags=["Фотографии"],
        request=serializers.ImageUploadSerializer,
        responses={status.HTTP_201_CREATED: {"type": "string"}},
    )
    def post(self, request, *args, **kwargs):
        file = request.FILES.get('file')
        if not file:
            return response.Response(
                {"detail": "No file provided."},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = request.user

        try:
            image = models.Image.objects.create(
                file=file,
                user=user,
                profile_order=models.Image.objects.filter(user__id=user.id).count() + 1,
            )

            return response.Response(
                {"detail": "Image uploaded successfully.", "url": image.url},
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return response.Response(
                {"detail": f"Failed to upload image: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
