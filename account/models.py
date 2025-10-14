from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):
    CATEGORY_CHOICES = [
        ('admin', 'Admin'),
        ('author', 'Author'),
        ('seller', 'Seller'),
        ('user', 'User')
    ]
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='user')
