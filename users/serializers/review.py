from rest_framework import serializers

from users.models import User


class UserReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "full_name", "profile_picture")
