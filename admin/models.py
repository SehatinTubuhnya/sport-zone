from django.db import models
from account.models import CustomUser

class ActionLog(models.Model):
    id = models.UUIDField(primary_key=True)
    actor = models.ForeignKey(CustomUser, null=False, on_delete=models.CASCADE)
    action = models.TextField(blank=False, null=False)
    timestamp = models.DateTimeField(null=False)
