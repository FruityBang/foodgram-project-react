from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE = [
        ('user', 'user'),
        ('moderator', 'moderator'),
        ('admin', 'admin'),
    ]
    role = models.CharField(
        max_length=40, choices=ROLE, default='user'
    )
    username = models.CharField(max_length=150, blank=False, unique=True)
    email = models.EmailField(max_length=254, blank=False, unique=True)
    first_name = models.CharField(max_length=150, blank=False)
    last_name = models.CharField(max_length=150, blank=False)
    last_name = models.CharField(max_length=150, blank=False)
    password = models.CharField(max_length=150, blank=False)
