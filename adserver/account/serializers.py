from django.conf import settings
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Wallet


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = '__all__'


class AccountSerializer(serializers.ModelSerializer):
    wallet = WalletSerializer()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'wallet', 'is_active', 'is_staff']
