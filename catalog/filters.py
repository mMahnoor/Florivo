from django_filters.rest_framework import FilterSet
from catalog.models import Flower


class FlowerFilter(FilterSet):
    class Meta:
        model = Flower
        fields = {
            'category_id': ['exact'],
            'price': ['gt', 'lt']
        }