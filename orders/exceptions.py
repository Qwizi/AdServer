from rest_framework.exceptions import APIException


class InvalidOrder(APIException):
    status_code = 400
    default_detail = "Invalid order"
    default_code = "invalid_order"
