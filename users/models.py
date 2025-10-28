from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
# from django.contrib.auth.models import Permission

from users.managers import CustomUserManager

# Create your models here.
class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    phone = PhoneNumberField(blank=True)
    address = models.TextField(blank=True, null=True)
    # role = models.ForeignKey("Role", null=True, blank=True, on_delete=models.SET_NULL)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

# class Role(models.Model):
    # name = models.CharField(max_length=50, unique=True)
    # permissions = models.ManyToManyField(Permission, blank=True)
    # created_by = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.SET_NULL, related_name='created_roles')

    # def __str__(self):
    #     return self.name