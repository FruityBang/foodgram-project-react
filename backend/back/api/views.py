from djoser.views import UserViewSet
from recipes.models import Ingredient, Recipe, Tag
from rest_framework import viewsets
from users.models import User

from .pagination import UserCustomPagination
from .serializers import (CustomUserSerializer, IngredientSerializer,
                          TagSerializer)


class CustomUserViewset(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    pagination_class = UserCustomPagination

