from rest_framework import serializers


class BriefProfileSerializer(serializers.Serializer):
    username = serializers.CharField(source='user.username', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    age = serializers.IntegerField(read_only=True)


class _ProfileImagesItem(serializers.Serializer):
    order = serializers.IntegerField()
    image = serializers.URLField()


class ProfileImagesSerializer(serializers.Serializer):
    username = serializers.CharField(read_only=True)
    images = serializers.ListField(child=_ProfileImagesItem(), default=[], read_only=True)
