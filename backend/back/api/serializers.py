from djoser.serializers import UserSerializer, TokenCreateSerializer
from rest_framework import serializers
from users.models import User


class CustomUserSerializer(UserSerializer):
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

#    def create(self, validated_data):
#        user = User(
#            email=validated_data['email'],
#            username=validated_data['username']
#        )
#        user.set_password(validated_data['password'])
#        user.save()
#        return user


class CustomTokenCreateSerializer(TokenCreateSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True
    )

    class Meta:
        model = User
        fields = (
            'password', 'email'
        )

#class UserSerializer(serializers.ModelSerializer):
#    password = serializers.CharField(
#        write_only=True,
#        required=True
#    )
#
#    class Meta:
#        model = User
#        fields = (
#            'email', 'id', 'username',
#            'first_name', 'last_name', 'password'
#        )
#
#
#class ChangePasswordSerializer(serializers.Serializer):
#    new_password = serializers.CharField(required=True)
#    current_password = serializers.CharField(required=True)
#
#    class Meta:
#        model = User
#