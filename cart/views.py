from rest_framework.permissions import IsAuthenticated
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from drf_yasg.utils import swagger_auto_schema

from cart.serializers import CartSerializer, CartItemSerializer, AddCartItemSerializer, UpdateCartItemSerializer
from cart.models import Cart, CartItem


# Create your views here.
class CartViewSet(ListModelMixin, CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericViewSet):
    """
    **Cart API**

    Manages flower shopping cart.

    - **GET /cart/** → List cart entry for the logged-in user  
    - **POST /cart/** → Create a new cart entry  
    - **GET /cart/{id}/** → Retrieve a specific cart  
    - **DELETE /cart/{id}/** → Delete a cart entry  

    Requires authentication.
    """
    
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Cart.objects.none()
        return Cart.objects.prefetch_related('items__flower').filter(user=self.request.user)

    @swagger_auto_schema(
        operation_summary="Retrieve cart created by the authenticated user",
        operation_description="Returns a list of all carts belonging to the current user."
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Add a new cart",
        operation_description="Adds a new cart for the authenticated user.",
        responses={201: CartSerializer()}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Retrieve a specific cart entry",
        operation_description="Retrieve a specific cart (and its items) belonging to the authenticated user.",
        responses={200: CartSerializer()}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Delete a cart entry",
        operation_description="Delete a specific cart (and its items) for the authenticated user.",
        responses={204: "Cart deleted successfully"}
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class CartItemViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if getattr(self, 'swagger_fake_view', False):
            return context

        return {'cart_id': self.kwargs.get('cart_pk')}

    def get_queryset(self):
        return CartItem.objects.select_related('flower').filter(cart_id=self.kwargs.get('cart_pk'))

    @swagger_auto_schema(
        operation_summary="Retrieve all cart items for the authenticated user",
        operation_description="Returns the specific cart with all its items belonging to the current user."
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Add a new item to the cart",
        operation_description="Adds a new cart items in the given cart.",
        responses={201: CartItemSerializer()}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Retrieve a specific item from the cart",
        operation_description="Retrieve a specific cart item belonging to the authenticated user.",
        responses={200: CartItemSerializer()}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Delete a cart item",
        operation_description="Delete a specific cart item from the given cart.",
        responses={204: "Cart item deleted successfully"}
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Partially update a cart",
        operation_description="Partially update the cart — for example, update quantities of items."
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
