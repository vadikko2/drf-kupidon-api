from rest_framework import serializers


class ProfileImagesItem(serializers.Serializer):
    order = serializers.IntegerField(read_only=True)
    url = serializers.URLField(read_only=True)


class ProfileImagesSerializer(serializers.Serializer):
    username = serializers.CharField(read_only=True)
    images = serializers.ListField(child=ProfileImagesItem(), default=[], read_only=True)
