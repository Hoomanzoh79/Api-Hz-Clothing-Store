from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from django.db import transaction

from orders.models import Order,OrderItem
from accounts.models import User,Profile
from cloths.models import Cloth
from cart.models import Cart,CartItem


class CustomerProfileSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField(method_name="get_email")
    class Meta:
        model = Profile
        fields = ["id","first_name", "last_name", "address","email"]
    
    def get_email(self,profile):
        return profile.user.email


class OrderClothSerializer(ModelSerializer):
    class Meta:
        model = Cloth
        fields = ["id","title","price"]


class OrderItemSerializer(ModelSerializer):
    cloth = OrderClothSerializer()
    class Meta:
        model = OrderItem
        fields = ["id","cloth","quantity","price"]
    

class OrderSerializer(ModelSerializer):
    customer = CustomerProfileSerializer()
    items = OrderItemSerializer(many=True,read_only=True)
    class Meta:
        model = Order
        fields = ["id","items","customer","is_paid",
                  "is_cancelled","datetime_created",]
        read_only_fields = ["customer"]
    
    def create(self, validated_data):
        request = self.context.get("request")
        validated_data["customer"] = User.objects.get(id=request.user.id)
        return super().create(validated_data)

class OrderCreateSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()

    def validate_cart_id(self,cart_id):
        try:
            if Cart.objects.prefetch_related("items").get(id=cart_id).items.count() == 0:
                raise serializers.ValidationError({"detail":"your cart is empty! please add some products first"})
        
        except Cart.DoesNotExist:
            raise serializers.ValidationError({"detail":"cart does not exist with the given id!"})
        
        return cart_id

    def save(self, **kwargs):
        with transaction.atomic():
            cart_id = self.validated_data["cart_id"]
            user_id = self.context["user_id"]
            customer = Profile.objects.get(user_id=user_id)

            order = Order()
            order.customer = customer
            order.save()

            cart_items = CartItem.objects.select_related("cloth").filter(cart_id=cart_id)

            order_items = list()
            for cart_item in cart_items:
                order_item = OrderItem()
                order_item.order = order
                order_item.cloth_id = cart_item.cloth_id
                order_item.price = cart_item.cloth.price
                order_item.quantity = cart_item.quantity

                order_items.append(order_item)
            
            OrderItem.objects.bulk_create(order_items)
            Cart.objects.get(id=cart_id).delete()
            return order

class OrderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["is_paid","is_cancelled",]