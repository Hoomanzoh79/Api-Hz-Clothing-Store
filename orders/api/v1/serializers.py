from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from orders.models import Order,OrderItem
from accounts.models import User
from cloths.models import Cloth


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
    items = OrderItemSerializer(many=True,read_only=True)
    total_price = serializers.SerializerMethodField(method_name="get_total_price")
    class Meta:
        model = Order
        fields = ["id","items","customer","is_paid",
                  "is_cancelled","first_name",
                  "last_name","phone_number",
                  "address","order_notes","datetime_created","total_price"]
        read_only_fields = ["customer"]
    
    def create(self, validated_data):
        request = self.context.get("request")
        validated_data["customer"] = User.objects.get(id=request.user.id)
        return super().create(validated_data)

    def get_total_price(self,order):
        return sum([item.quantity * item.cloth.price for item in order.items.all()])