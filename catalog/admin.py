from django.contrib import admin
from catalog.models import Flower, Category, FlowerImage

# Register your models here.

admin.site.register(Flower)
admin.site.register(FlowerImage)
admin.site.register(Category)