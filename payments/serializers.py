from rest_framework import serializers


class PaymentSerializer(serializers.Serializer):
    order_id = serializers.UUIDField(required=True, format="hex")

class CreatePaymentMethodSerializer(serializers.Serializer):
    payment_method_id = serializers.CharField(max_length=27, required=True)
