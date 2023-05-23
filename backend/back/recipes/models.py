from django.db import models


class Tag(models.Model):
    name = models.CharField('Название', max_length=256)
    slug = models.SlugField('Уникальный адрес', max_length=50, unique=True)
    color = models.CharField(max_length=16)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField('Название', max_length=256)
    measurement_unit = models.CharField('Единица измерения', max_length=256)

    def __str__(self):
        return self.name
