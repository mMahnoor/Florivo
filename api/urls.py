from django.urls import path, include
from rest_framework_nested import routers

from catalog.views import CategoryViewSet, FlowerImageViewSet, FlowerViewSet
from orders.views import OrderViewset
from cart.views import CartViewSet, CartItemViewSet

router = routers.DefaultRouter()
router.register('flowers', FlowerViewSet, basename='flowers')
router.register('categories', CategoryViewSet)
router.register('carts', CartViewSet, basename='carts')
router.register('orders', OrderViewset, basename='orders')

flower_router = routers.NestedDefaultRouter(
    router, 'flowers', lookup='flower')
flower_router.register('images', FlowerImageViewSet,
                        basename='flower-images')

cart_router = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
cart_router.register('items', CartItemViewSet, basename='cart-item')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(flower_router.urls)),
    path('', include(cart_router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]
