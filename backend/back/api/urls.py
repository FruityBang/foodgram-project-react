from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CustomUserViewset, IngredientViewSet,
                    RecipeViewSet, TagViewSet)

router = DefaultRouter()

router.register('users', CustomUserViewset)
router.register('ingredients', IngredientViewSet)
router.register('tags', TagViewSet)
router.register('recipes', RecipeViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
