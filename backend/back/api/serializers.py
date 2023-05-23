from djoser.serializers import UserCreateSerializer
from djoser.serializers import UserSerializer
# from djoser.serializers import TokenCreateSerializer
from rest_framework import serializers
from users.models import User
# from djoser.conf import settings
# from django.contrib.auth import authenticate
from recipes.models import Tag, Ingredient
import webcolors


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

#    def create(self, validated_data):
#        user = User(
#            email=validated_data['email'],
#            username=validated_data['username']
#        )
#        user.set_password(validated_data['password'])
#        user.save()
#        return user


# class CustomTokenCreateSerializer(TokenCreateSerializer):
#     password = serializers.CharField(
#         required=False, style={'input_type': 'password'}
#         )
# 
#     default_error_messages = {
#         "invalid_credentials": (
#               settings.CONSTANTS.messages.INVALID_CREDENTIALS_ERROR),
#         "inactive_account": (
#               settings.CONSTANTS.messages.INACTIVE_ACCOUNT_ERROR),
#     }
# 
#     def __init__(self, *args, **kwargs):
#         super(TokenCreateSerializer, self).__init__(*args, **kwargs)
#         self.user = None
#         self.fields[User.EMAIL_FIELD] = serializers.EmailField(
#             required=False
#         )
# 
#     def validate(self, attrs):
#         self.user = authenticate(
#             email=attrs.get(User.EMAIL_FIELD),
#             password=attrs.get('password')
#             )
# 
#         self._validate_user_exists(self.user)
#         self._validate_user_is_active(self.user)
#         return attrs
# 
#     def _validate_user_exists(self, user):
#         if not user:
#             self.fail('invalid_credentials')
# 
#     def _validate_user_is_active(self, user):
#         if not user.is_active:
#             self.fail('inactive_account')

# class UserSerializer(serializers.ModelSerializer):
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
# class ChangePasswordSerializer(serializers.Serializer):
#    new_password = serializers.CharField(required=True)
#    current_password = serializers.CharField(required=True)
#
#    class Meta:
#        model = User
#


class Hex2NameColor(serializers.Field):
    def to_representation(self, value):
        return value

    def to_internal_value(self, data):
        try:
            return webcolors.hex_to_name(data)
        except ValueError:
            raise serializers.ValidationError('Для этого цвета нет имени')


class TagSerializer(serializers.ModelSerializer):
    color = Hex2NameColor()

    class Meta:
        model = Tag
        fields = (
            'id', 'name', 'color', 'slug'
        )


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = (
            'id', 'name', 'measurement_unit'
        )