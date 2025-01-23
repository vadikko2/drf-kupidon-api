from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import authentication, permissions, views
from rest_framework.response import Response

from profiles import models
from profiles.serializers import images


@extend_schema(
    parameters=[
        OpenApiParameter("username", type=str, description="Логин пользователя", required=True),
    ],
    responses={200: images.ProfileImagesSerializer},
)
class ProfileImagesView(views.APIView):
    serializer_class = images.ProfileImagesSerializer
    authentication_classes = [authentication.SessionAuthentication, authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        username = request.GET.get('username')
        if not username:
            return Response({"detail": "Username parameter is required."}, status=400)

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
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)
