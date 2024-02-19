from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db.models import Prefetch


from .permissions import OrderIsAdminOrReadOnly,OrderItemIsAdminOrReadOnly
from .serializers import OrderSerializer,OrderItemSerializer
from orders.models import Order,OrderItem
from accounts.models import Profile


class OrderViewSet(ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Order.objects.prefetch_related(
                Prefetch("items",
                         queryset=OrderItem.objects.select_related("cloth"),
                         )
            ).select_related("customer__user").filter(is_cancelled=False)
        user = self.request.user
        if user.is_staff & user.is_superuser:
            return queryset
        
        return queryset.filter(customer__user_id=user.id)



class OrderItemViewSet(ModelViewSet):
    serializer_class = OrderItemSerializer
    queryset = OrderItem.objects.all()
    permission_classes = [IsAuthenticated]
        