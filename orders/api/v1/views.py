from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated,DjangoModelPermissions
from .permissions import IsAdminOrReadOnly


from .serializers import OrderSerializer,OrderItemSerializer
from orders.models import Order,OrderItem


class OrderViewSet(ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated,IsAdminOrReadOnly]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser & user.is_staff:
            return Order.objects.prefetch_related("items__cloth").select_related("customer").filter(is_cancelled=False)
        else:
            return Order.objects.prefetch_related("items__cloth").select_related("customer").filter(is_cancelled=False,customer=user)


class OrderItemViewSet(ModelViewSet):
    serializer_class = OrderItemSerializer
    queryset = OrderItem.objects.all()
        