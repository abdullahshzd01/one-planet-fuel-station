from rest_framework import serializers

from APIs.Serializers.ProductSerializer import productsSerializer
from app.models import *



class OrderSerializer(serializers.ModelSerializer):
    products = productsSerializer(read_only=True,many=True)
    class Meta:
        model = order
        fields = "__all__"
