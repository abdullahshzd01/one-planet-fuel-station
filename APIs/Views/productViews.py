from django.db.models import Q
from django.http import JsonResponse
from rest_framework import generics, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from APIs.Serializers.ProductSerializer import productsSerializer
from app.models import *


class ProductsList(generics.ListAPIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
    queryset = products.objects.all()
    serializer_class = productsSerializer

    def get_queryset(self):
        queryset = products.objects.all()
        title = self.request.query_params.get('title', None)
        if title is not None:
            queryset = queryset.filter(Q(title__icontains=title))
        stationID = self.request.query_params.get('stationID', None)
        if stationID is not None:
            queryset = queryset.filter(Q(fuelStation__id=stationID))
        return queryset


class ProductDetail(generics.RetrieveAPIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
    queryset = products.objects.all()
    serializer_class = productsSerializer

    def get_object(self):
        id = self.kwargs.get('pk')
        return products.objects.get(pk=id)


class ProductRatingCreateUpdate(generics.CreateAPIView, generics.UpdateAPIView, generics.ListAPIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
    queryset = ProductRatings.objects.all()
    serializer_class = productsSerializer

    def create(self, request, *args, **kwargs):
        # try:
        productID = request.data['product']
        email = request.data['email']
        user = None
        productID = products.objects.get(id=productID)
        if users.objects.filter(email=email).exists():
            user = users.objects.get(email=email)
        else:
            user = users()
            user.email = email
            user.firstName = email.split('@')[0]
            user.lastName = email.split('@')[0]
            user.phone = email.split('@')[0]
            user.save()
        rating = request.data['rating']
        if ProductRatings.objects.filter(product=productID, user=user).exists():
            ProductRatings.objects.filter(product=productID, user=user).update(rating=rating)
        else:
            ProductRatings.objects.create(product=productID, user=user, rating=rating)
        return Response(status=status.HTTP_201_CREATED)

        # except Exception as e:
        #     return Response(status=status.HTTP_400_BAD_REQUEST)
