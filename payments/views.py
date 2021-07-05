from django.conf import settings
from django.core.exceptions import BadRequest
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
import stripe

from orders.exceptions import InvalidOrder
from orders.models import Order
from payments.serializers import PaymentSerializer

stripe.api_key = settings.STRIPE_API_KEY


def create_customer(email, payment_method_id):
    # checking if customer with provided email already exists
    customer_data = stripe.Customer.list(email=email).data

    # if the array is empty it means the email has not been used yet
    if len(customer_data) == 0:
        # creating customer
        customer = stripe.Customer.create(
            email=email, payment_method=payment_method_id)
    else:
        customer = customer_data[0]

    return customer


class PaymentsViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request):
        serializer = PaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        order_id = serializer.validated_data['order_id']
        payment_method_id = serializer.validated_data['payment_method_id']

        print(order_id)

        if not Order.objects.filter(id=order_id, user=user).exists():
            raise InvalidOrder

        order = Order.objects.get(id=order_id, user=user)
        customer = create_customer(order.user.email, payment_method_id)
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

        return Response(data={"status": "success"}, status=status.HTTP_200_OK)

    @action(detail=False, methods=["POST"])
    def webhook(self, request):
        print(request.data)
        return Response(status=status.HTTP_204_NO_CONTENT)