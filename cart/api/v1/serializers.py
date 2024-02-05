from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from cart.models import Cart,CartItem
from cloths.models import Cloth



class CartProductSerializer(ModelSerializer):
    class Meta:
        model = Cloth
        fields = ["id","title","price"]

class CartItemSerializer(ModelSerializer):
    cloth = CartProductSerializer()
    item_total = serializers.SerializerMethodField(method_name="get_item_total")
    class Meta:
        model = CartItem
        fields = ["cart","cloth","quantity","item_total"]
    
    def get_item_total(self,cart_item):
        return (cart_item.quantity * cart_item.cloth.price)

class CartSerializer(ModelSerializer):
    items = CartItemSerializer(many=True,read_only=True)
    total_price = serializers.SerializerMethodField(method_name="get_total_price")
    class Meta:
        model = Cart
        fields = ["id","items","total_price"]
        read_only_fields = ["id"]
    
    def get_total_price(self,cart):
        for item in cart.items.all():
            return sum([item.quantity * item.cloth.price])