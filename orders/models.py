from django.db import models
from accounts.models import Profile

class Order(models.Model):
    customer = models.ForeignKey(Profile, on_delete=models.PROTECT,related_name="orders")
    is_paid = models.BooleanField(default=False)
    is_cancelled = models.BooleanField(default=False)

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    address = models.CharField(max_length=700)
    order_notes = models.CharField(max_length=700, blank=True)

    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Order {self.id}'

    def get_total_price(self):
        return sum(item.price * item.quantity for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='items')
    cloth = models.ForeignKey('cloths.Cloth', on_delete=models.PROTECT, related_name='order_items')
    quantity = models.PositiveSmallIntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        unique_together = [['order', 'cloth']]

    def __str__(self):
        return f'OrderItem {self.id}: {self.cloth} x {self.quantity} (price:{self.price})'

