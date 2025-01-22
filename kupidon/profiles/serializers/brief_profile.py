from rest_framework import serializers


class BriefProfileSerializer(serializers.Serializer):
    username = serializers.CharField(source='user.username', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    age = serializers.IntegerField(read_only=True)
    profile_image = serializers.URLField(read_only=True)
    distance_km = serializers.IntegerField(read_only=True, default=None, allow_null=True)
    compatibility = serializers.FloatField(read_only=True, min_value=0, max_value=100, allow_null=False)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        distance = self.context.get('distance_km')
        if distance is not None:
            representation['distance_km'] = round(distance, 2)  # Округляем до двух знаков после запятой
        return representation
