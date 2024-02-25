from django.dispatch import receiver
from orders.signals import order_created


# Create a profile after a user is created
@receiver(order_created)
def after_order_created(sender, **kwargs):
    print(f'New order is created : {kwargs["order"].id}')