from django_filters.rest_framework import FilterSet
from catalog.models import Plant


class PlantFilter(FilterSet):
    class Meta:
        model = Plant
        fields = {
            'category_id': ['exact'],
            'price': ['gt', 'lt']
        }