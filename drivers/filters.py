import django_filters

from .models import Driver


class DriverFilter(django_filters.FilterSet):
    from_region_name = django_filters.CharFilter(field_name="from_region__name", lookup_expr="icontains")
    to_region_name = django_filters.CharFilter(field_name="to_region__name", lookup_expr="icontains")

    class Meta:
        model = Driver
        fields = ["from_region_name", "to_region_name", "status"]

