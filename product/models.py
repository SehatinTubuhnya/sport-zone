from django.db import models
from account.models import CustomUser

CATEGORY_CHOICES = [
    ('equipment', 'Equipment'),
    ('apparel', 'Apparel'),
    ('ball', 'Ball'),
]

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.TextField()
    category = models.CharField(
        max_length=100,
        choices=CATEGORY_CHOICES,
        default='equipment'
    )
    thumbnail = models.URLField(blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name
