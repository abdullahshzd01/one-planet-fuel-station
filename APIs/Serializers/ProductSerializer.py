from rest_framework import serializers
from .FuelStationSerializer import FuelStationSerializer
from app.models import *


class productsSerializer(serializers.ModelSerializer):

    imageURL = serializers.SerializerMethodField()
    fuelStation = FuelStationSerializer(read_only=True)
    rating = serializers.SerializerMethodField()

    def get_rating(self, obj):

        ratings = ProductRatings.objects.filter(product=obj)
        if ratings.count() == 0:
            return {
                "rating": 3.5,
                "count": ratings.count()

            }
        else:
            sum = 0
            for rating in ratings:
                sum += rating.rating
            return {
                "rating": sum / ratings.count(),
                "count": ratings.count()

            }

    def get_imageURL(self, obj):
        if obj.image is not None:
            return obj.image.url
        else:
            return ""


    class Meta:
        model = products
        fields = "__all__"


class ProductRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductRatings
        fields = "__all__"
        extra_kwargs = {
            "user": {"required": False, "allow_null": True},
        }


class FavProductSerializer(serializers.ModelSerializer):
    product = productsSerializer(read_only=True)
    class Meta:
        model = ProductFavs
        fields = "__all__"
        extra_kwargs = {
            "user": {"required": False, "allow_null": True},
        }