from django.db import models
from uuid import uuid4

class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(primary_key=True,default=uuid4)