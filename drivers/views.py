from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from permissions.custom_permission import IsOwnerOrReadOnly
from users.models import User
from utils.paginations import CustomPageNumberPagination
from .filters import DriverFilter
from .models import Driver
from .serializers import DriverCreateSerializer, DriverSerializer, DriverUpdateSerializer


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
    pagination_class = CustomPageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = DriverFilter

    def get_queryset(self):
        return Driver.objects.select_related('user', 'from_region', 'to_region')


class DriverProfileView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DriverUpdateSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_object(self):
        try:
            return Driver.objects.get(user=self.request.user)
        except Driver.DoesNotExist:
            raise NotFound("Haydovchilikka ariza topshirgan profil mavjud emas.")

    def delete(self, request, *args, **kwargs):
        driver = Driver.objects.get(user=self.request.user)
        driver.delete()
        self.request.user.status = "passenger"
        self.request.user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
