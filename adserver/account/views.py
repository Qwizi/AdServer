import stripe
from rest_framework import viewsets, mixins
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from account.exceptions import WalletNoFunds
from ads.models import Ad, AdStatsView, AdStatsClick
from ads.serializers import AdSerializer, AdUpdateSerializer, AdChargeSerializer, AdStatsViewSerializer, \
    AdStatsClickSerializer
from orders.models import Order
from orders.serializers import OrderSerializer
from payments.exceptions import PaymentMethodAlreadySet
from payments.serializers import CreatePaymentMethodSerializer
from payments.stripe import create_customer, get_customer


class AccountAdViewSet(viewsets.ModelViewSet):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Ad.objects.filter(user=self.request.user)

    def get_serializer_class(self, *args, **kwargs):
        serializer_class = self.serializer_class

        if self.request.method == 'PUT':
            serializer_class = AdUpdateSerializer
        return serializer_class

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['PUT'])
    def charge(self, request, pk=None):
        serializer = AdChargeSerializer(data=request.data)
        if serializer.is_valid():
            ad = self.get_object()
            wallet = request.user.wallet
            value = serializer.validated_data['value']

            if wallet.balance < value:
                raise WalletNoFunds()

            wallet.debit(value)
            ad.charge(value)

            wallet.save()
            ad.save()

            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AccountAdStatsViewViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = AdStatsView.objects.all()
    serializer_class = AdStatsViewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return AdStatsView.objects.filter(ad__user=self.request.user, ad__id=self.kwargs['ad_pk'])


class AccountAdStatsClickViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = AdStatsClick.objects.all()
    serializer_class = AdStatsClickSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return AdStatsClick.objects.filter(ad__user=self.request.user, ad__id=self.kwargs['ad_pk'])


class AccountOrdersViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AccountPaymentMethodViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request):
        serializer = CreatePaymentMethodSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payment_method_id = serializer.validated_data['payment_method_id']

        if request.user.wallet.customer_id is not None:
            raise PaymentMethodAlreadySet

        customer = create_customer(request.user.email, payment_method_id)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def list(self, request):
        data = stripe.PaymentMethod.list(customer=get_customer(request.user.email), type="card")
        return Response(data=data.data, status=status.HTTP_200_OK)

