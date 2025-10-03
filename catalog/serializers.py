from rest_framework import serializers
from decimal import Decimal
from catalog.models import Category, Plant, PlantImage

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'plant_count']

    plant_count = serializers.IntegerField(
        read_only = True, 
    )

class PlantImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()

    class Meta:
        model = PlantImage
        fields = ['id', 'image']

class PlantSerializer(serializers.ModelSerializer):
    plant_images = PlantImageSerializer(many=True)

    class Meta:
        model = Plant
        fields = ['id', 'title', 'description', 'price', 'category', 'is_available', 'seller', 'stock', 'plant_images']

    def validate_price(self, price):
        if price < 0:
            raise serializers.ValidationError('Price could not be negative')
        return price

