from django.db import models


class Tag(models.Model):
    name = models.CharField('Название', max_length=256)
    slug = models.SlugField('Уникальный адрес', max_length=50, unique=True)
    color = models.CharField(max_length=16)
