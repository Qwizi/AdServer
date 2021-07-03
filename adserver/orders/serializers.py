from rest_framework import serializers

from orders.models import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'user', 'name', 'status', 'amount', 'created_at', 'stripe_id']
        read_only_fields = ['user', 'name', 'status', 'created_at', 'stripe_id']
