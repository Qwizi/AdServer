from rest_framework.exceptions import APIException


class WalletNoFunds(APIException):
    status_code = 400
    default_detail = "Wallet no founds"
    default_code = "wallet_no_funds"
