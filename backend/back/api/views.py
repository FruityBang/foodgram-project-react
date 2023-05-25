from djoser.views import UserViewSet
from users.models import User

from .pagination import UserCustomPagination
from .serializers import CustomUserSerializer


class CustomUserViewset(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    pagination_class = UserCustomPagination
