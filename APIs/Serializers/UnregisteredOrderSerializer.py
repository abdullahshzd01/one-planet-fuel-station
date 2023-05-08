from rest_framework import serializers

from APIs.Serializers.ProductSerializer import productsSerializer
from app.models import *



class UnregesteredOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = unregisteredOrders
        fields = "__all__"
        extra_kwargs = {
            "Customer": {"required": False, "allow_null": True},

        }