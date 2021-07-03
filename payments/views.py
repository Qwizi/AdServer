from django.conf import settings
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
import stripe

stripe.api_key = settings.STRIPE_API_KEY


class PaymentsViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request):
        user = request.user
        payment_method_id = request.data['payment_method_id']
        # checking if customer with provided email already exists
        customer_data = stripe.Customer.list(email=user.email).data

        # if the array is empty it means the email has not been used yet
        if len(customer_data) == 0:
            # creating customer
            customer = stripe.Customer.create(
                email=user.email, payment_method=payment_method_id)
        else:
            customer = customer_data[0]
            extra_msg = "Customer already existed."

        print(customer_data)
        return Response(status=status.HTTP_200_OK, data={"costumer.id": customer.id})
