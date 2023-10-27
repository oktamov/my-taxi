from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User
from utils.verification import check_verification_code, get_verification_type


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "phone_number", "birth_date", "profile_picture")


class TokenObtainPairSerializer(TokenObtainSerializer):  # noqa
    token_class = RefreshToken

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        data["user"] = UserSerializer(self.user, context={"request": self.context["request"]}).data

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data


class UserRegisterSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField()

    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "phone_number", "profile_picture"]

    def to_representation(self, instance):
        data = instance.tokens()
        data["user"] = UserSerializer(instance, context={"request": self.context["request"]}).data
        return data


class UserLoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=20)
    code = serializers.CharField(max_length=6)

    def create(self, validated_data):
        phone_number = validated_data.get("phone_number")
        code = validated_data.get("code")
        verification_type = get_verification_type(phone_number)

        if not check_verification_code(phone_number, verification_type, code):
            raise ValidationError("Incorrect verification code.")

        user = User.objects.filter(phone_number=phone_number).first()

        if not user:
            raise ValidationError("User with this phone number does not exist.")

        refresh = RefreshToken.for_user(user)
        user_serializer = UserSerializer(user)
        tokens_and_user_data = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": user_serializer.data
        }
        return tokens_and_user_data
