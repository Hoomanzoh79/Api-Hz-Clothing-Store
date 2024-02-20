from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db.models import Prefetch

from .serializers import (OrderSerializer,OrderItemSerializer,OrderCreateSerializer)
from orders.models import Order,OrderItem
from accounts.models import Profile


class OrderViewSet(ModelViewSet):
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
    
    def get_serializer_class(self):
        if self.request.method == "POST":
            return OrderCreateSerializer
        
        return OrderSerializer
    
    def get_serializer_context(self):
        return {"user_id":self.request.user.id}


class OrderItemViewSet(ModelViewSet):
    serializer_class = OrderItemSerializer
    queryset = OrderItem.objects.all()
    permission_classes = [IsAuthenticated]
        