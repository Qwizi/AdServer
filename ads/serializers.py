from abc import ABC

from rest_framework import serializers

from .models import Ad


class AdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = ['id', 'user', 'name', 'url', 'banner', 'balance', 'is_active']
        read_only_fields = ['user', 'balance', 'is_active']


class AdUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = ['name', "url", "banner"]
        extra_kwargs = {
            'name': {
                'required': False
            },
            'url': {
                'required': False
            },
            'banner': {
                'required': False
            },
        }


class AdChargeSerializer(serializers.Serializer):
    value = serializers.DecimalField(max_digits=6, decimal_places=2)
