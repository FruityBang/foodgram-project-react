from django.urls import include, path
from rest_framework.routers import DefaultRouter




urlpatterns = [
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
