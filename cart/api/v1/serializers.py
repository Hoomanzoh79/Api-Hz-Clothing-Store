from rest_framework.serializers import ModelSerializer
from cart.models import Cart,CartItem



class CartItemSerializer(ModelSerializer):
    class Meta:
        model = CartItem
        fields = ["cart","cloth","quantity"]


class CartSerializer(ModelSerializer):
    items = CartItemSerializer(many=True)
    class Meta:
        model = Cart
        fields = ["id","items"]
        read_only_fields = ["id","items"]