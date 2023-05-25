
from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from users.models import User


class CustomUserSerializer(UserCreateSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True
    )

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username',
            'first_name', 'last_name', 'password'
        )
