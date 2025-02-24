from rest_framework import serializers

from images import models


class ProfileImagesItem(serializers.Serializer):
    order = serializers.IntegerField()
    url = serializers.URLField()


class ProfileImagesSerializer(serializers.Serializer):
    username = serializers.CharField()
    images = serializers.ListField(child=ProfileImagesItem(), default=[])


class ImageUploadSerializer(serializers.Serializer):
    class Meta:
        model = models.Image
        fields = ('profile_order', 'file',)
