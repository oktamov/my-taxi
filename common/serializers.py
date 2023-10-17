from rest_framework import serializers

from .models import Country, Region


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ("name", "dial_code", "code")


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ("name", "country")
