from django.db import models
from users.models import User


class Tag(models.Model):

    BLUE = "#0000FF"
    RED = "#FF0000"
    GREEN = "#008000"
    YELLOW = "#FFFF00"

    COLOR_CHOICES = [
        (BLUE, "Синий"),
        (RED, "Красный"),
        (GREEN, "Зелёный"),
        (YELLOW, "Жёлтый"),
    ]

    name = models.CharField('Тэг', max_length=20, unique=True)
    slug = models.SlugField('Уникальный адрес', max_length=200, unique=True)
    color = models.CharField(
        max_length=7,
        choices=COLOR_CHOICES,
        unique=True,
        verbose_name="Цвет",
    )

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField("Ингредиент", max_length=200)
    measurement_unit = models.CharField("Единица измерения", max_length=20)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return f"{self.name}, {self.measurement_unit}"


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="recipes"
    )
    tags = models.ManyToManyField(
        Tag, through="TagsInRecipe", related_name="recipes"
    )
    name = models.CharField('Название', max_length=256)
    text = models.TextField('Описание')
    cooking_time = models.PositiveSmallIntegerField()
    ingredients = models.ManyToManyField(
        Ingredient,
        through="IngredientInRecipe",
        related_name="recipes",
        blank=True,
    )
    pub_date = models.DateTimeField(
        auto_now_add=True, verbose_name="Время публикации"
    )
    image = models.ImageField()

    class Meta:
        ordering = ["-pub_date"]
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"

    def __str__(self):
        return self.name


class TagsInRecipe(models.Model):

    tag = models.ForeignKey(
        Tag, verbose_name="Тег в рецепте", on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = "Теги в рецепте"
        verbose_name_plural = verbose_name


class IngredientInRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name="Ингредиент в рецепте",
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, verbose_name="Рецепт"
    )
    amount = models.PositiveIntegerField(
        null=True, verbose_name="Количество ингредиента"
    )

    class Meta:
        verbose_name = "Количетсво ингредиента в рецепте"
        verbose_name_plural = verbose_name
