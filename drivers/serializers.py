from rest_framework import serializers

from common.models import Region
from users.serializers import UserSerializer
from .models import Driver


class DriverCreateSerializer(serializers.ModelSerializer):
    from_region = serializers.CharField()
    to_region = serializers.CharField()

    class Meta:
        model = Driver
        fields = ('from_region', 'to_region', 'price', 'car', 'car_number', 'seats', 'status')

    def create(self, validated_data):
        user = self.context['request'].user

        if user.status == 'driver':
            raise serializers.ValidationError('You are already a driver')

        validated_data['user'] = user
        from_regions, _ = Region.objects.get_or_create(name=validated_data.pop('from_region'))
        to_regions, _ = Region.objects.get_or_create(name=validated_data.pop('to_region'))
        validated_data['from_region'] = from_regions
        validated_data['to_region'] = to_regions
        driver = super().create(validated_data)
        user.status = 'driver'
        user.save()
        return driver


class DriverSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Driver
        fields = ('id', 'from_region', 'to_region', 'price', 'car', 'car_number', 'seats', 'status', 'user')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['from_region'] = instance.from_region.name
        data['to_region'] = instance.to_region.name
        return data


class DriverUpdateSerializer(serializers.ModelSerializer):
    from_region = serializers.CharField()
    to_region = serializers.CharField()

    class Meta:
        model = Driver
        fields = ('from_region', 'to_region', 'price', 'car', 'car_number', 'seats', 'status')

    def update(self, instance, validated_data):
        instance.price = validated_data.get('price', instance.price)
        instance.car = validated_data.get('car', instance.car)
        instance.car_number = validated_data.get('car_number', instance.car_number)
        instance.seats = validated_data.get('seats', instance.seats)
        instance.status = validated_data.get('status', instance.status)

        from_region_name = validated_data.get('from_region')
        to_region_name = validated_data.get('to_region')

        if from_region_name:
            from_region, _ = Region.objects.get_or_create(name=from_region_name)
            instance.from_region = from_region

        if to_region_name:
            to_region, _ = Region.objects.get_or_create(name=to_region_name)
            instance.to_region = to_region

        instance.save()
        return instance

    def delete(self, instance):
        user = instance.user
        user.status = 'passenger'
        user.save()

        instance.delete()
