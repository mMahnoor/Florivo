from django.urls import path, include
from rest_framework_nested import routers

from catalog.views import CategoryViewSet, PlantImageViewSet, PlantViewSet
from orders.views import OrderViewset
from cart.views import CartViewSet, CartItemViewSet

router = routers.DefaultRouter()
router.register('plants', PlantViewSet, basename='plants')
router.register('categories', CategoryViewSet)
router.register('carts', CartViewSet, basename='carts')
router.register('orders', OrderViewset, basename='orders')

plant_router = routers.NestedDefaultRouter(
    router, 'plants', lookup='plant')
plant_router.register('images', PlantImageViewSet,
                        basename='plant-images')

cart_router = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
cart_router.register('items', CartItemViewSet, basename='cart-item')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(plant_router.urls)),
    path('', include(cart_router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]
