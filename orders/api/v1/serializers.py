from rest_framework.serializers import ModelSerializer
from orders.models import Order,OrderItem

class OrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = ["id","customer","is_paid",
                  "is_cancelled","first_name",
                  "last_name","phone_number",
                  "address","order_notes","datetime_created"]