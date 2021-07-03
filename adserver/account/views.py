from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from account.exceptions import WalletNoFunds
from ads.models import Ad
from ads.serializers import AdSerializer, AdUpdateSerializer, AdChargeSerializer


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
