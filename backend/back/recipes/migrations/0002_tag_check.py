# Generated by Django 3.2 on 2023-05-31 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_recipes_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='color',
            field=models.CharField(max_length=7, unique=True),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=256, verbose_name='Тэги'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='slug',
            field=models.SlugField(unique=True, verbose_name='Уникальный адрес'),
        ),
    ]
