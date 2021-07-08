import json
import locale
import pprint
from collections import namedtuple

from django.conf import settings
from django.core.exceptions import BadRequest
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status, views
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from .stripe import stripe, create_customer, get_customer

from orders.exceptions import InvalidOrder
from orders.models import Order, OrderStatus
from payments.serializers import PaymentSerializer


class PaymentsView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
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


class PaymentsWebhookView(views.APIView):

    def post(self, request):
        data = request.data
        event = namedtuple("Event", data.keys())(*data.values())

        if event.type == "payment_intent.succeeded":
            event_data = event.data['object']
            order_id = event_data['metadata']['order_id']

            order = get_object_or_404(Order, pk=order_id)

            if order.status == OrderStatus.PAID:
                raise InvalidOrder

            formatted_amount = order.get_formatted_amount()

            wallet = order.user.wallet
            wallet.recharge(formatted_amount)
            wallet.save()

            order.status = OrderStatus.PAID
            order.save()

            print("Zakonczono platnosc")

        return Response(status=status.HTTP_204_NO_CONTENT)
