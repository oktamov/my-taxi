from rest_framework import serializers

from common.models import Region
from users.serializers import UserSerializer
from .models import Driver


class DriverCreateSerializer(serializers.ModelSerializer):
    from_region = serializers.CharField()
    to_region = serializers.CharField()

    class Meta:
        model = Driver
        fields = ('from_region', 'to_region', 'price', 'car', 'car_number', 'status')

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        from_regions, _ = Region.objects.get_or_create(name=validated_data.pop('from_region'))
        to_regions, _ = Region.objects.get_or_create(name=validated_data.pop('to_region'))
        validated_data['from_region'] = from_regions
        validated_data['to_region'] = to_regions
        driver = super().create(validated_data)
        return driver


class DriverSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Driver
        fields = ('id', 'from_region', 'to_region', 'price', 'car', 'car_number', 'status', 'user')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['from_region'] = instance.from_region.name
        data['to_region'] = instance.to_region.name
        return data
