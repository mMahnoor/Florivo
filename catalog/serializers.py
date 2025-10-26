from rest_framework import serializers
from catalog.models import Category, Flower, FlowerImage

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'flower_count']

    flower_count = serializers.IntegerField(
        read_only = True, 
    )

class FlowerImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()

    class Meta:
        model = FlowerImage
        fields = ['id', 'image']

class FlowerSerializer(serializers.ModelSerializer):
    flower_images = FlowerImageSerializer(many=True, read_only=True)

    class Meta:
        model = Flower
        fields = ['id', 'title', 'description', 'price', 'category', 'is_available', 'seller', 'stock', 'flower_images']
        read_only = ['seller']

    def validate_price(self, price):
        if price < 0:
            raise serializers.ValidationError('Price could not be negative')
        return price
