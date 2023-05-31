import base64

import webcolors
from django.core.files.base import ContentFile
from djoser.serializers import UserSerializer
from recipes import models
from rest_framework import serializers, validators
from users.models import Follow, User

# USERS&FOLLOW vol.


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        if (self.context.get('request')
           and not self.context['request'].user.is_anonymous):
            return Follow.objects.filter(user=self.context['request'].user,
                                         author=obj).exists()
        return False


class RecipeFollowSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class FollowListSerializer(serializers.ModelSerializer):
    email = serializers.ReadOnlyField(source='author.email')
    id = serializers.ReadOnlyField(source='author.id')
    username = serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = Follow
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        )

    def get_is_subscribed(self, obj):
        return Follow.objects.filter(
            user=self.context['request'].user, author=obj.author
        ).exists()

    def get_recipes_count(self, obj):
        return obj.author.recipes.count()

    def get_recipes(self, obj):
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        recipes = models.Recipe.objects.filter(
                author=obj.author)
        if limit:
            recipes = recipes[:int(limit)]
        serializer = RecipeFollowSerializer(
            recipes, read_only=True, many=True
        )
        return serializer.data


class FollowCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Follow
        fields = ('user', 'author')
        validators = [
            validators.UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'author'),
                message="Двойная подписка"
            )
        ]

    def validate_following(self, value):
        if self.context['request'].user == value:
            raise serializers.ValidationError(
                'Подписка на себя'
            )
        return value

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        serializer = FollowListSerializer(
            instance,
            context=context
        )
        return serializer.data

# RECIPES vol.


class TagColorField(serializers.Field):
    def to_representation(self, value):
        return value

    def to_internal_value(self, data):
        try:
            data = webcolors.hex_to_name(data)
        except ValueError:
            raise serializers.ValidationError('Для этого цвета нет имени')


class TagSerializer(serializers.ModelSerializer):
    color = TagColorField()

    class Meta:
        model = models.Tag
        fields = ('id', 'name', 'slug', 'color')


class TagToRecipe(serializers.SlugRelatedField):

    class Meta:
        model = models.Tag
        fields = ('id')

    def to_representation(self, value):
        context = {'request': self.context.get('request')}
        serializer = TagSerializer(value, context=context)
        return serializer.data


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Ingredient
        fields = ('id', 'name', 'measurement_unit')


class RecipeIngredientListSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = models.RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeIngredientCreateSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=models.Ingredient.objects.all()
    )
    amount = serializers.IntegerField()

    class Meta:
        model = models.RecipeIngredient
        fields = ('id', 'amount')


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class RecipeListSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    tags = TagToRecipe(
        slug_field='id', queryset=models.Tag.objects.all(), many=True
    )
    ingredients = RecipeIngredientListSerializer(
        source='ingredient_for_recipe',
        read_only=True, many=True
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField()

    class Meta:
        model = models.Recipe
        fields = (
            'id',
            'tags',
            'name',
            'author',
            'ingredients',
            'image',
            'text',
            'cooking_time',
            'is_favorited',
            'is_in_shopping_cart'
        )

    def get_bool(self, obj, model):
        if self.context.get('request'):
            return (
                self.context.get('request').user.is_authenticated
                and model.objects.filter(user=self.context.get('request').user,
                                         recipe=obj).exists()
            )
        return False

    def get_is_favorited(self, obj):
        return self.get_bool(obj, models.Favorite)

    def get_is_in_shopping_cart(self, obj):
        return self.get_bool(obj, models.ShoppingCart)


class RecipeCreateSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        queryset=models.Tag.objects.all(),
        many=True
    )
    ingredients = RecipeIngredientCreateSerializer(many=True)
    image = Base64ImageField()

    class Meta:
        model = models.Recipe
        fields = (
            'tags',
            'name',
            'ingredients',
            'image',
            'text',
            'cooking_time'
        )

    def add_ingredients(self, recipe, ingredients):
        for ingredient in ingredients:
            ingredient, _ = models.RecipeIngredient.objects.get_or_create(
                recipe=recipe,
                ingredient=ingredient['id'],
                amount=ingredient['amount']
            )

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = models.Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        recipe.save()
        self.add_ingredients(recipe, ingredients)
        return recipe

    def update(self, instance, validated_data):
        instance.image = validated_data.get('image', instance.image)
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time)
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        models.RecipeIngredient.objects.filter(
            recipe=instance,
            ingredient__in=instance.ingredients.all()).delete()
        self.add_ingredients(instance, ingredients)
        instance.tags.set(tags)
        instance.save()
        return instance

    def to_representation(self, instance):
        serializer = RecipeListSerializer(instance, context=self.context)
        return serializer.data
