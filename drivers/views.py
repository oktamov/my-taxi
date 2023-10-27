from django.db.models import Prefetch
from rest_framework import generics, permissions

from .models import Driver
from .serializers import DriverCreateSerializer, DriverSerializer


class DriverCreateView(generics.CreateAPIView):
    serializer_class = DriverCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Driver.objects.select_related('user', 'from_region', 'to_region')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DriverListView(generics.ListAPIView):
    serializer_class = DriverSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Driver.objects.select_related('user', 'from_region', 'to_region')
