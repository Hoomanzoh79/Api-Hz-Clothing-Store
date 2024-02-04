from django.db import models
from uuid import uuid4
from cloths.models import Cloth

class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(primary_key=True,default=uuid4)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    cloth = models.ForeignKey(Cloth, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = [['cart', 'cloth']]