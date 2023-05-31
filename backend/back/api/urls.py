from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register('ingredients', views.IngredientViewSet)
router.register('recipes', views.RecipeViewSet)
router.register('tags', views.TagViewSet, basename='tags')

urlpatterns = [
    path('users/subscriptions/', views.FollowListView.as_view()),
    path('users/<int:pk>/subscribe/', views.CreateFollowView.as_view()),
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken'))
]
