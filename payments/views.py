from django.conf import settings
from django.core.exceptions import BadRequest
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from .stripe import stripe, create_customer, get_customer

from orders.exceptions import InvalidOrder
from orders.models import Order, OrderStatus
from payments.serializers import PaymentSerializer


class PaymentsViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request):
        serializer = PaymentSerializer(data=request.data)

        if serializer.is_valid():
            user = request.user
            order_id = serializer.validated_data['order_id']

            if not Order.objects.filter(id=order_id, user=user).exists():
                raise InvalidOrder

            order = Order.objects.get(id=order_id, user=user)

            if order.status == OrderStatus.PAID:
                raise InvalidOrder

            customer = get_customer(user.email)
            payment_method_id = stripe.PaymentMethod.list(customer=customer['id'], type="card").data[0].id

            payment_intent = stripe.PaymentIntent.create(
                customer=customer,
                payment_method=payment_method_id,
                currency='pln',
                amount=order.amount,
                metadata={'order_id': order.id},
                confirm=True
            )
            payment_intent_id = payment_intent['id']

            order.stripe_id = payment_intent_id
            order.save()

            return Response(data={"status": "success"}, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["POST"])
    def webhook(self, request):
        print(request.data)
        return Response(status=status.HTTP_204_NO_CONTENT)