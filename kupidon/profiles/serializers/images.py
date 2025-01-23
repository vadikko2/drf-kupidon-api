from rest_framework import serializers


class ProfileImagesItem(serializers.Serializer):
    order = serializers.IntegerField()
    url = serializers.URLField()


class ProfileImagesSerializer(serializers.Serializer):
    username = serializers.CharField()
    images = serializers.ListField(child=ProfileImagesItem(), default=[])
