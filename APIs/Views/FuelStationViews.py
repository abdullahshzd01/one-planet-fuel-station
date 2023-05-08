from django.db.models import Q
from django.http import JsonResponse
from rest_framework import generics, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from APIs.Serializers.CartSerializer import CartSerializer
from APIs.Serializers.FuelStationSerializer import FuelStationSerializer
from APIs.Serializers.ProductSerializer import productsSerializer
from app.models import *


class FuelStation(generics.ListAPIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
    queryset = fuelStations.objects.all()
    serializer_class = FuelStationSerializer

    def get_queryset(self):
        queryset = fuelStations.objects.all()
        name = self.request.query_params.get('title', None)
        if name is not None:
            queryset = queryset.filter(Q(name__icontains=name))

        return queryset


class FuelStationDetail(generics.RetrieveAPIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
    queryset = fuelStations.objects.all()
    serializer_class = FuelStationSerializer

    def get_object(self):
        id = self.kwargs.get('pk')
        return fuelStations.objects.get(pk=id)