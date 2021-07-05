from rest_framework.exceptions import APIException


class PaymentMethodAlreadySet(APIException):
    status_code = 400
    default_detail = "Payment method already set"
    default_code = "payment_method_already_set"
