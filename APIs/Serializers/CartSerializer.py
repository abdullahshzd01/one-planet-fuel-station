from rest_framework import serializers

from APIs.Serializers.ProductSerializer import productsSerializer
from app.models import *



class CartSerializer(serializers.ModelSerializer):
    products = productsSerializer(read_only=True,many=True)
    class Meta:
        model = cart
        fields = "__all__"
        extra_kwargs = {
            "user": {"required": False, "allow_null": True},

        }
