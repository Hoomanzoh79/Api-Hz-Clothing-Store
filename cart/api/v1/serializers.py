from rest_framework.serializers import ModelSerializer
from cart.models import Cart,CartItem


class CartSerializer(ModelSerializer):
    class Meta:
        model = Cart
        fields = ["id",]
        read_only_fields = ["id"]