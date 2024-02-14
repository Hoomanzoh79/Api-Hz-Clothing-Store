from rest_framework.serializers import ModelSerializer
from orders.models import Order,OrderItem
from accounts.models import User

class OrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = ["id","customer","is_paid",
                  "is_cancelled","first_name",
                  "last_name","phone_number",
                  "address","order_notes","datetime_created"]
        read_only_fields = ["customer"]
    
    def create(self, validated_data):
        request = self.context.get("request")
        validated_data["customer"] = User.objects.get(id=request.user.id)
        return super().create(validated_data)