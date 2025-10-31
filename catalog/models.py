from django.db import models
from django.contrib.auth import get_user_model
from catalog.validators import validate_file_size

User = get_user_model()

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    
class Flower(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='flowers')
    title = models.CharField(max_length=150)
    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.SET_NULL, related_name='flowers')
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self): 
        return self.title

class FlowerImage(models.Model):
    flower = models.ForeignKey(Flower, on_delete=models.CASCADE, related_name="flower_images")
    image = models.ImageField(upload_to="florivo/catalog_images/", default="media/florivo/image_icon_fsvtyo", validators=[validate_file_size])

    def __str__(self): 
        return f"Image for {self.flower.title}"