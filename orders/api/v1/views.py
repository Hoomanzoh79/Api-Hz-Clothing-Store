from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from django.db.models import Prefetch
from rest_framework.response import Response

from .serializers import (OrderSerializer,OrderItemSerializer,
                          OrderCreateSerializer,OrderUpdateSerializer,OrderForAdminSerializer)
from orders.models import Order,OrderItem
from orders.signals import order_created


class OrderViewSet(ModelViewSet):
    http_method_names = ["get","post","patch","delete","options","head"]

    def get_permissions(self):
        if self.request.method in ["PATCH","DELETE"]:
            return [IsAdminUser()]
        return [IsAuthenticated()]
    
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
        if self.request.method == "PATCH":
            return OrderUpdateSerializer
        if self.request.user.is_staff & self.request.user.is_superuser:
            return OrderForAdminSerializer
        
        return OrderSerializer
    
    def get_serializer_context(self):
        return {"user_id":self.request.user.id}

    def create(self, request, *args, **kwargs):
        create_order_serializer = OrderCreateSerializer(data=request.data,
                                                        context={"user_id":self.request.user.id},
                                                        )
        create_order_serializer.is_valid(raise_exception=True)
        created_order = create_order_serializer.save()

        order_created.send_robust(self.__class__,order=created_order)

        serializer = OrderSerializer(created_order)
        return Response(serializer.data)

class OrderItemViewSet(ModelViewSet):
    serializer_class = OrderItemSerializer
    queryset = OrderItem.objects.all()
    permission_classes = [IsAuthenticated]
        