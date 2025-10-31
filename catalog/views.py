from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from drf_yasg.utils import swagger_auto_schema
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count

from catalog.models import Category, Flower, FlowerImage
from catalog.serializers import CategorySerializer, FlowerImageSerializer, FlowerSerializer
from catalog.filters import FlowerFilter
from catalog.paginations import DefaultPagination
from api.permissions import IsSellerOrAdminOrReadOnly

# Create your views here.

class CategoryViewSet(ModelViewSet):
    """
    Manage catalog categories:
    - View all flower categories
    - Only admin and seller can create, update or delete categories
    """
    queryset = Category.objects.annotate(
        flower_count=Count('flowers')).all()
    serializer_class = CategorySerializer
    permission_classes = [IsSellerOrAdminOrReadOnly]

class FlowerViewSet(ModelViewSet):
    """
    API endpoint for managing catalog
     - Allows authenticated admin to create, update, and delete a catalog item
     - Allows users to browse and filter catalog item
     - Support searching by name, description, and category
     - Support ordering by price and name
    """
    serializer_class = FlowerSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = FlowerFilter
    pagination_class = DefaultPagination
    search_fields = ['title', 'description']
    ordering_fields = ['title', 'price']
    permission_classes = [IsSellerOrAdminOrReadOnly]

    # def get_serializer_class(self):
    #     if self.action in ["create", "update", "partial_update"]:
    #         return CatalogItemCreateSerializer
    #     return PlantSerializer
    def get_queryset(self):
        return Flower.objects.prefetch_related('flower_images').all()
    
    @swagger_auto_schema(
        operation_summary="Retrieve all flowers",
        operation_description="Returns the the list of all flowers in the catalog."
    )
    def list(self, request, *args, **kwargs):
        """Retrive all the flowers list"""
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create a new flower listing",
        # operation_description="Returns the the list of all flowers in the catalog."
    )
    def create(self, request, *args, **kwargs):
        """Only authenticated seller or admin can create a new catalog item which is flower listing."""
        return super().create(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        """Automatically assign the current user in the seller field."""
        serializer.save(seller=self.request.user)

    @swagger_auto_schema(
        operation_summary="Retrieve a specific flower instance",
        operation_description="Returns the details of a specific flower instance."
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    
class FlowerImageViewSet(ModelViewSet):
    """
    Manage Flower images:
    - Get all images for a specific flower or catalog item
    - Add images for a specific catalog item
    - Retrive image of a flower by image id
    - Update a specific image by id
    - Delete an image by id
    """
    serializer_class = FlowerImageSerializer
    permission_classes = [IsSellerOrAdminOrReadOnly]

    def get_queryset(self):
        # print("from getQ img: ", self.kwargs)
        return FlowerImage.objects.filter(flower_id=self.kwargs.get('flower_pk'))

    def perform_create(self, serializer):
        # print("from getQ img: ", self.kwargs)
        serializer.save(flower_id=self.kwargs.get('flower_pk'))
