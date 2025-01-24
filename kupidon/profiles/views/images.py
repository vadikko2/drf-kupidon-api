from django.contrib.auth import models as auth_models
from drf_spectacular import utils
from rest_framework import authentication, generics, permissions, response, status

from profiles import models
from profiles.serializers import images


@utils.extend_schema(
    parameters=[
        utils.OpenApiParameter("username", type=str, description="Логин пользователя", required=True),
    ],
    responses={status.HTTP_200_OK: images.ProfileImagesSerializer},
)
class ProfileImagesView(generics.GenericAPIView):
    serializer_class = images.ProfileImagesSerializer
    authentication_classes = [authentication.SessionAuthentication, authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]

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

        serializer = self.serializer_class(data={
            'username': username,
            'images': images_data,
        })

        if serializer.is_valid():
            return response.Response(serializer.data)
        else:
            return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
