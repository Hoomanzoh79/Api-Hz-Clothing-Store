from rest_framework.serializers import ModelSerializer
from cart.models import Cart,CartItem
from cloths.models import Cloth



class CartProductSerializer(ModelSerializer):
    class Meta:
        model = Cloth
        fields = ["id","title","price"]


class CartItemSerializer(ModelSerializer):
    cloth = CartProductSerializer()
    class Meta:
        model = CartItem
        fields = ["cart","cloth","quantity"]


class CartSerializer(ModelSerializer):
    items = CartItemSerializer(many=True,read_only=True)
    class Meta:
        model = Cart
        fields = ["id","items"]
        read_only_fields = ["id" ]