from django.contrib import admin
from catalog.models import Plant, Category, PlantImage

# Register your models here.

admin.site.register(Plant)
admin.site.register(PlantImage)
admin.site.register(Category)