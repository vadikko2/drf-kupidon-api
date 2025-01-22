from datetime import date

from rest_framework import serializers


class BriefProfileSerializer(serializers.Serializer):
    username = serializers.CharField(source='user.username', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True, max_length=12)
    last_name = serializers.CharField(source='user.last_name', read_only=True, allow_null=True, default=None)
    age = serializers.IntegerField(read_only=True)
    profile_image = serializers.URLField(read_only=True)
    security_level = serializers.FloatField(read_only=True, min_value=0, max_value=100)
    description = serializers.CharField(read_only=True, allow_null=True, default=None, max_length=100)
    last_login = serializers.DateTimeField(source='user.last_login', read_only=True, allow_null=True, default=None)
    online = serializers.BooleanField(read_only=True, default=False)

    distance_km = serializers.FloatField(read_only=True, default=None, allow_null=True)
    compatibility = serializers.FloatField(read_only=True, min_value=0, max_value=100, allow_null=False)

    def get_age(self, obj):
        """Вычисляет возраст на основе даты рождения."""
        if obj.birthdate:
            today = date.today()
            age = today.year - obj.birthdate.year
            if (today.month, today.day) < (obj.birthdate.month, obj.birthdate.day):
                age -= 1
            return age
        return None

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['age'] = self.get_age(instance)
        distance = self.context.get('distance_km')

        if distance is not None:
            representation['distance_km'] = round(distance, 2)
        return representation
