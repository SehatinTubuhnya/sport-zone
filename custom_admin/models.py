from django.db import models
from account.models import CustomUser
import uuid

class ActionLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    actor = models.CharField(max_length=150, null=False)
    action = models.TextField(blank=False, null=False)
    timestamp = models.DateTimeField(null=False, auto_now_add=True)
