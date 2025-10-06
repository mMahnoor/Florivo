from django.urls import path, include
from rest_framework_nested import routers

from catalog.views import CategoryViewSet, PlantImageViewSet, PlantViewSet

router = routers.DefaultRouter()
router.register('plants', PlantViewSet, basename='plants')
router.register('categories', CategoryViewSet)

plant_router = routers.NestedDefaultRouter(
    router, 'plants', lookup='plant')
plant_router.register('images', PlantImageViewSet,
                        basename='plant-images')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(plant_router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]
