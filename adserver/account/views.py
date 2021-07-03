from rest_framework import viewsets
from rest_framework import permissions

from ads.models import Ad
from ads.serializers import AdSerializer, AdUpdateSerializer


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
