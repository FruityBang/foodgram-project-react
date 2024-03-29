from django.conf import settings
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, status, views, viewsets
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from recipes.models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                            ShoppingCart, Tag)
from users.models import Follow, User

from . import serializers
from .filters import CustomFilter, IngredientsFilter
from .pagination import CustomPaginator
from .permissions import IsOwnerOrReadOnly


class FollowListView(ListAPIView):
    serializer_class = serializers.FollowListSerializer
    pagination_class = CustomPaginator
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.request.user.follower.all()


class CreateFollowView(views.APIView):
    pagination_class = CustomPaginator
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk):
        author = get_object_or_404(User, pk=pk)
        serializer = serializers.FollowCreateSerializer(
            data={'author': author.id, 'user': self.request.user.id},
            context={'request': request}
        )
        serializer.is_valid()
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        get_object_or_404(
            Follow,
            user=self.request.user,
            author=get_object_or_404(User, pk=pk)
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TagViewSet(mixins.ListModelMixin,
                 mixins.RetrieveModelMixin,
                 viewsets.GenericViewSet):
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer
    permission_classes = (AllowAny,)
    pagination_class = None


class IngredientViewSet(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer
    permission_classes = (AllowAny,)
    filterset_class = IngredientsFilter


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (IsOwnerOrReadOnly,)
    pagination_class = CustomPaginator
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CustomFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return serializers.RecipeListSerializer
        return serializers.RecipeCreateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def create_model(self, model, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        model.objects.create(recipe=recipe, user=self.request.user)
        serializer = serializers.RecipeFollowSerializer(recipe)
        return Response(
            data=serializer.data, status=status.HTTP_201_CREATED)

    def delete_model(self, model, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        model = get_object_or_404(model, recipe=recipe, user=self.request.user)
        model.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=('post', 'delete'),
        permission_classes=(IsAuthenticated,)
    )
    def favorite(self, request, pk=None):
        if request.method == 'DELETE':
            return self.delete_model(Favorite, request, pk)
        return self.create_model(Favorite, request, pk)

    @action(
        detail=True,
        methods=('post', 'delete'),
        permission_classes=(IsAuthenticated,)
    )
    def shopping_cart(self, request, pk):
        if request.method == 'DELETE':
            return self.delete_model(ShoppingCart, request, pk)
        return self.create_model(ShoppingCart, request, pk)

    @action(
        detail=False,
        methods=('get',),
        permission_classes=(IsAuthenticated,)
    )
    def download_shopping_cart(self, request):
        ingredients = (
            RecipeIngredient.objects
            .filter(recipe__shopping_cart__user=request.user)
            .values('ingredient__name', 'ingredient__measurement_unit')
            .annotate(ingredient_total=Sum('amount'))
            .order_by('ingredient__name')
        )
        file_list = []
        for ingredient in ingredients:
            name = ingredient['ingredient__name']
            measurement_unit = ingredient['ingredient__measurement_unit']
            amount = ingredient['ingredient_total']
            file_list.append(f'{name} ({measurement_unit}) - {amount}')

        file = HttpResponse('\n'.join(file_list), content_type='text/plain')
        file['Content-Disposition'] = (f'attachment; '
                                       f'filename={settings.FILE_NAME}')
        return file
