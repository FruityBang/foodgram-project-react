from django.db import models
from users.models import User


class Tag(models.Model):
    name = models.CharField('Тэги', max_length=256)
    slug = models.SlugField('Уникальный адрес', max_length=50, unique=True)
    color = models.CharField(max_length=16)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField('Ингредиенты', max_length=256)
    measurement_unit = models.CharField('Единица измерения', max_length=256)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField('Рецепты', max_length=256, blank=False)
    tags = models.ManyToManyField(Tag, through='TagRecipe', related_name='recipes')
    image = models.ImageField(upload_to='recipes/images/', null=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    text = models.TextField('Описание', blank=False)
#    ingredients = models.ManyToManyField(
#        Ingredient,
#        through='RecipeIngredient',
#        blank=True
#    )
    cooking_time = models.PositiveSmallIntegerField(blank=False)

    def __str__(self):
        return self.name


class TagRecipe(models.Model):
    tag = models.ForeignKey(
        Tag, on_delete=models.CASCADE, related_name='tagrecipes'
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='tagrecipes'
    )
