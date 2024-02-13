from rest_framework.viewsets import ModelViewSet


from .serializers import OrderSerializer
from orders.models import Order,OrderItem


class OrderViewSet(ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.filter(is_cancelled=False)
        