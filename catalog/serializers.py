from rest_framework import serializers
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
    plant_images = PlantImageSerializer(many=True, read_only=True)

    class Meta:
        model = Plant
        fields = ['id', 'title', 'description', 'price', 'category', 'is_available', 'seller', 'stock', 'plant_images']

    def validate_price(self, price):
        if price < 0:
            raise serializers.ValidationError('Price could not be negative')
        return price

# class CatalogItemCreateSerializer(serializers.ModelSerializer):
#     images = serializers.ListField(
#         child=serializers.ImageField(),
#         write_only=True,
#         required=False
#     )

#     class Meta:
#         model = Plant
#         fields = ["title", "description", "price", "category", "images"]

#     def validate_images(self, value):
#         if len(value) > 6:
#             raise serializers.ValidationError("You can upload up to 6 images.")
#         return value

#     def create(self, validated_data):
#         images = validated_data.pop("images", [])
#         catalogItem = Plant.objects.create(**validated_data)
#         for img in images:
#             PlantImage.objects.create(listing=catalogItem, image=img)
#         return catalogItem
    
