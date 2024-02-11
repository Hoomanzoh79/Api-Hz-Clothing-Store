from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework.viewsets import ModelViewSet

from .serializers import (CartSerializer,
                          CartItemSerializer,
                          AddCartItemSerializer,
                          UpdateCartItemSerializer)

from cart.models import Cart,CartItem


class CartItemViewSet(ModelViewSet):
    http_method_names = ["get","post","patch","delete"]
    
    def get_queryset(self):
        cart_pk = self.kwargs["cart_pk"]
        return CartItem.objects.select_related("cloth").filter(cart_id=cart_pk).all()
    
    def get_serializer_class(self):
        if self.request.method=="POST":
            return AddCartItemSerializer
        
        elif self.request.method=="PATCH":
            return UpdateCartItemSerializer
        
        return CartItemSerializer
    
    def get_serializer_context(self):
        return {"cart_pk":self.kwargs["cart_pk"]}

class CartViewSet(mixins.CreateModelMixin,
                  mixins.DestroyModelMixin,
                   mixins.RetrieveModelMixin,
                   GenericViewSet):
    
    serializer_class = CartSerializer
    queryset = Cart.objects.prefetch_related("items__cloth").all() 