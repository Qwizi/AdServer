import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_API_KEY


def get_customer(email):
    return stripe.Customer.list(email=email).data[0]


def create_customer(email, payment_method_id):
    # checking if customer with provided email already exists
    customer_data = get_customer(email)

    # if the array is empty it means the email has not been used yet
    if len(customer_data) == 0:
        # creating customer
        customer = stripe.Customer.create(
            email=email, payment_method=payment_method_id)
    else:
        customer = customer_data[0]

    return customer
