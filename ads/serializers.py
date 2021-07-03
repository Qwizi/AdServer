from rest_framework import serializers

from .models import Ad


class AdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = ['id', 'user', 'name', 'url', 'banner', 'balance', 'is_active']
        read_only_fields = ['user', 'balance', 'is_active']