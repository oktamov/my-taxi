from rest_framework import serializers

from utils.regex import phone_regex


class SendVerificationCodeSerializer(serializers.Serializer):  # noqa
    phone_number = serializers.CharField(validators=[phone_regex])


class PhoneVerifySerializer(serializers.Serializer):  # noqa
    phone_number = serializers.CharField(validators=[phone_regex])
    code = serializers.CharField(min_length=6, max_length=6)
