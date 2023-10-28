from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions

from permissions.custom_permission import IsOwnerOrReadOnly
from users.filters import AnnouncementFilter
from users.models.announcement import Announcement
from users.serializers import AnnouncementCreateSerializer, AnnouncementSerializer, AnnouncementUpdateSerializer
from utils.paginations import CustomPageNumberPagination


class AnnouncementCreateView(generics.CreateAPIView):
    serializer_class = AnnouncementCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Announcement.objects.select_related('user', 'from_region', 'to_region')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AnnouncementListView(generics.ListAPIView):
    serializer_class = AnnouncementSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = AnnouncementFilter

    def get_queryset(self):
        return Announcement.objects.select_related('user', 'from_region', 'to_region')


class AnnouncementProfileView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementUpdateSerializer
    permission_classes = [IsOwnerOrReadOnly]
