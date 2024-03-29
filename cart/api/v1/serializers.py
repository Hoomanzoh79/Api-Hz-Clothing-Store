from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from cart.models import Cart,CartItem
from cloths.models import Cloth


class CartProductSerializer(ModelSerializer):
    class Meta:
        model = Cloth
        fields = ["id","title","price"]

class UpdateCartItemSerializer(ModelSerializer):
    class Meta:
        model = CartItem
        fields = ["quantity"]
class AddCartItemSerializer(ModelSerializer):
    class Meta:
        model = CartItem
        fields = ["id","cloth","quantity"]

    def create(self, validated_data):
        cart_id = self.context["cart_pk"]
        cloth = validated_data.get("cloth")
        quantity = validated_data.get("quantity")

        try:
            cart_item = CartItem.objects.get(cart_id=cart_id,cloth_id=cloth.id)
            cart_item.quantity += quantity
            cart_item.save()

        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(cart_id=cart_id,**validated_data)

        self.instance = cart_item
        return cart_item

class CartItemSerializer(ModelSerializer):
    cloth = CartProductSerializer()
    item_total = serializers.SerializerMethodField(method_name="get_item_total")
    class Meta:
        model = CartItem
        fields = ["id","cloth","quantity","item_total"]
    
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
        return sum([item.quantity * item.cloth.price for item in cart.items.all()])