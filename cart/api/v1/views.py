from rest_framework import mixins
from .serializers import CartSerializer
from cart.models import Cart,CartItem
from rest_framework.viewsets import GenericViewSet

class CartViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   GenericViewSet):
    
    serializer_class = CartSerializer
    queryset = Cart.objects.prefetch_related("items__cloth").all()