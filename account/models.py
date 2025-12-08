from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    profile_pic = models.URLField(null=True)
    birth_date = models.DateField(null=False, default="2025-01-01")
    is_author = models.BooleanField(null=False, default=False)
    is_seller = models.BooleanField(null=False, default=False)

    @property
    def is_admin(self):
        return self.is_staff

    @is_admin.setter
    def is_admin(self, value):
        self.is_staff = value
