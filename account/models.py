from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):
    is_admin = models.BooleanField(null=False, default=False)
    is_author = models.BooleanField(null=False, default=False)
    is_seller = models.BooleanField(null=False, default=False)
