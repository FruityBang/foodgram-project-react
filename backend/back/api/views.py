from djoser.views import UserViewSet
from recipes.models import Ingredient, Recipe, Tag
from rest_framework import viewsets
from users.models import User

from .pagination import UserCustomPagination
from .serializers import (CustomUserSerializer, IngredientSerializer,
                          RecipeSerializer, TagSerializer)


class CustomUserViewset(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    pagination_class = UserCustomPagination


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
