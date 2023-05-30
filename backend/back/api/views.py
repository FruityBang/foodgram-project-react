from django.shortcuts import render
from djoser.views import UserViewSet
from .serializers import CustomUserSerializer
from .pagination import CustomPagination
from users.models import User


class CustomUserViewset(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    pagination_class = CustomPagination
