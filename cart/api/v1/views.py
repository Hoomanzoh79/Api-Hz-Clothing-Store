from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework.viewsets import ModelViewSet

from .serializers import CartSerializer,CartItemSerializer
from cart.models import Cart,CartItem


class CartItemViewSet(ModelViewSet):
    serializer_class = CartItemSerializer
    
    def get_queryset(self):
        cart_pk = self.kwargs["cart_pk"]
        return CartItem.objects.select_related("cloth").filter(cart_id=cart_pk).all()

class CartViewSet(mixins.CreateModelMixin,
                  mixins.DestroyModelMixin,
                   mixins.RetrieveModelMixin,
                   GenericViewSet):
    
    serializer_class = CartSerializer
    queryset = Cart.objects.prefetch_related("items__cloth").all()