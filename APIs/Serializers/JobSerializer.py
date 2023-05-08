from rest_framework import serializers
from .FuelStationSerializer import FuelStationSerializer
from app.models import *


class JobsSerializer(serializers.ModelSerializer):
    fuelStation = FuelStationSerializer(read_only=True)

    class Meta:
        model = jobs
        fields = "__all__"
