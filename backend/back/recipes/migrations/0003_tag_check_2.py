# Generated by Django 3.2 on 2023-05-31 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_tag_check'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=256, verbose_name='Тэг'),
        ),
    ]
