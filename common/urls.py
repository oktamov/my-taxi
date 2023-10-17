from django.urls import path

from .views import CountryListView, RegionViewSet


urlpatterns = [
    path("countries/", CountryListView.as_view(), name="country-list"),
    path("regions/", RegionViewSet.as_view(), name="region-list"),
]
