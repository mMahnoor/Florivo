from rest_framework import serializers

from cart.models import Cart, CartItem
from catalog.models import Plant

class SimpleCatalogItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plant
        fields = ['id', 'title', 'price']

class AddCartItemSerializer(serializers.ModelSerializer):
    plant_id = serializers.IntegerField()

    class Meta:
        model = CartItem
        fields = ['id', 'plant_id', 'quantity']

    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        plant_id = self.validated_data['plant_id']
        quantity = self.validated_data['quantity']

        try:
            cart_item = CartItem.objects.get(cart_id=cart_id, plant_id=plant_id)
            cart_item.quantity += quantity
            self.instance = cart_item.save()
        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(
                cart_id=cart_id, **self.validated_data)

        return self.instance

    def validate_product_id(self, value):
        if not Plant.objects.filter(pk=value).exists():
            raise serializers.ValidationError(f"Catalog item with id {value} does not exists")
        return value


class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']


class CartItemSerializer(serializers.ModelSerializer):
    plant = SimpleCatalogItemSerializer()
    total_price = serializers.SerializerMethodField(method_name='get_total_price')

    class Meta:
        model = CartItem
        fields = ['id', 'plant', 'quantity', 'plant', 'total_price']

    def get_total_price(self, cart_item: CartItem):
        return cart_item.quantity * cart_item.plant.price
    
class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField(method_name='get_total_price')

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'total_price']
        read_only_fields = ['user']

    def get_total_price(self, cart: Cart):
        return sum([item.plant.price * item.quantity for item in cart.items.all()])
