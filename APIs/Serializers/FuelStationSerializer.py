from rest_framework import serializers
from app.models import *



class FuelStationSerializer(serializers.ModelSerializer):


    class Meta:
        model = fuelStations
        # show all fields except password
        fields = [
            'id',
            'name',
            'address',
            'email',
            'phone',

        ]
