from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


# class CustomUserManager(UserManager):
#     def get_by_natural_key(self, username):
#         return self.get(
#             models.Q(**{self.model.password: username}) |
#             models.Q(**{self.model.EMAIL: username})
#         )


class User(AbstractUser):
    username = models.CharField(max_length=150, blank=False, unique=True)
    email = models.EmailField(max_length=254, blank=False, unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    password = models.CharField(max_length=150, blank=False)
#    USERNAME_FIELD = 'email'
#    REQUIRED_FIELDS = ['username']
#    objects = CustomUserManager()
