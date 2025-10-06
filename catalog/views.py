from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count

from catalog.models import Category, Plant, PlantImage
from catalog.serializers import CategorySerializer, PlantImageSerializer, PlantSerializer
from catalog.filters import PlantFilter
from catalog.paginations import DefaultPagination

# Create your views here.

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.annotate(
        plant_count=Count('plants')).all()
    serializer_class = CategorySerializer

class PlantViewSet(ModelViewSet):
    """
    API endpoint for managing plants catalog
     - Allows authenticated admin to create, update, and delete a catalog item
     - Allows users to browse and filter plants
     - Support searching by name, description, and category
     - Support ordering by price and name
    """
    queryset = Plant.objects.all()
    serializer_class = PlantSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = PlantFilter
    pagination_class = DefaultPagination
    search_fields = ['title', 'description']
    ordering_fields = ['title', 'price']

    # def get_serializer_class(self):
    #     if self.action in ["create", "update", "partial_update"]:
    #         return CatalogItemCreateSerializer
    #     return PlantSerializer
    
    def list(self, request, *args, **kwargs):
        """Retrive all the plants list"""
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """Only authenticated admin can create a new catalog item"""
        return super().create(request, *args, **kwargs)
    
class PlantImageViewSet(ModelViewSet):
    serializer_class = PlantImageSerializer

    def get_queryset(self):
        print("from getQ img: ", self.kwargs)
        return PlantImage.objects.filter(plant_id=self.kwargs.get('plant_pk'))

    def perform_create(self, serializer):
        print("from getQ img: ", self.kwargs)
        serializer.save(plant_id=self.kwargs.get('plant_pk'))
