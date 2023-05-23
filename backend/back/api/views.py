from djoser.views import UserViewSet
from rest_framework import viewsets
# from rest_framework import generics
# from rest_framework import status
# from rest_framework.response import Response
from recipes.models import Ingredient, Tag
from users.models import User

from .serializers import (
    CustomUserSerializer, IngredientSerializer, TagSerializer
)


class CustomUserViewset(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer

# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#
#
# class ChangePasswordView111(generics.UpdateAPIView):
#     serializer_class = ChangePasswordSerializer
#
#     def get_object(self, queryset=None):
#         return self.request.user
#
#     def update(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         serializer = self.get_serializer(data=request.data)
#
#         if serializer.is_valid():
#             if not self.object.check_password(
#                 serializer.data.get("current_password")
#             ):
#                 return Response({"current_password": "ur mistaken fella"})
#             self.object.set_password(serializer.data.get("new_password"))
#             self.object.save()
#             return Response(status=status.HTTP_204_NO_CONTENT)
#         return Response(status=status.HTTP_400_BAD_REQUEST)
#
#
# class ChangePasswordView(generics.CreateAPIView):
#     serializer_class = ChangePasswordSerializer
#
#     def get_object(self, queryset=None):
#         return self.request.user
#
#     def create(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         serializer = self.get_serializer(data=request.data)
#
#         if serializer.is_valid():
#             if not self.object.check_password(
#                 serializer.data.get("current_password")
#             ):
#                 return Response({"current_password": "ur mistaken fella"})
#             self.object.set_password(serializer.data.get("new_password"))
#             self.object.save()
#             return Response(status=status.HTTP_204_NO_CONTENT)
#         return Response(status=status.HTTP_400_BAD_REQUEST)
#


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
