from datetime import date

from drf_extra_fields import geo_fields
from rest_framework import serializers

from profiles import models


class PutProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Profile
        fields = '__all__'  # Или явный список полей
        read_only_fields = ('user', 'created_at')  # Запрещаем изменение системных полей
        extra_kwargs = {
            'last_location': {'write_only': True},  # Пример дополнительных настроек
        }

    def create(self, validated_data):
        # Автоматически связываем профиль с пользователем
        return models.Profile.objects.create(
            user=self.context['request'].user,
            **validated_data
        )

    def update(self, instance, validated_data):
        # Автоматическое обновление всех разрешенных полей
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class GetBriefProfileSerializer(serializers.Serializer):
    username = serializers.CharField(source='user.username')
    first_name = serializers.CharField(source='user.first_name', max_length=12)
    last_name = serializers.CharField(source='user.last_name', allow_null=True, default=None)
    profile_image = serializers.URLField()

    age = serializers.IntegerField(allow_null=True, default=None)
    last_login = serializers.DateTimeField(source='user.last_login', allow_null=True, default=None)
    security_level = serializers.FloatField(min_value=0, max_value=100)
    description = serializers.CharField(allow_null=True, default=None, max_length=100)

    online = serializers.BooleanField(default=False)

    distance_km = serializers.FloatField(default=None, allow_null=True)

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
