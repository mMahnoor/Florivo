from django.urls import path, include
from rest_framework import routers

from catalog.views import CategoryViewSet, PlantViewSet

router = routers.DefaultRouter()
router.register('plants', PlantViewSet, basename='plants')
router.register('categories', CategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]
