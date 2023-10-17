from rest_framework import generics

from common.models import Country, Region
from common.serializers import CountrySerializer, RegionSerializer
from paginations import CustomPageNumberPagination


class CountryListView(generics.ListAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    pagination_class = CustomPageNumberPagination


class RegionViewSet(generics.ListAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    pagination_class = CustomPageNumberPagination
