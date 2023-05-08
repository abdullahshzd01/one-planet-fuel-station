from django.db.models import Q
from django.http import JsonResponse
from rest_framework import generics, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from APIs.Serializers import UnregisteredOrderSerializer
from APIs.Serializers.CartSerializer import CartSerializer
from APIs.Serializers.OrderSerializer import OrderSerializer
from APIs.Serializers.ProductSerializer import productsSerializer
from app.models import *


@api_view(['POST'])
def addItemToCart(request):
    try:
        print(request.data)
        prID = request.data['productID']
        print(prID)
        product = products.objects.get(pk=int(prID))
        # check if cart exists
        email = request.data['email']
        user = None
        if users.objects.filter(email=email).exists():
            user = users.objects.get(email=email)
        else:
            user = users()
            user.email = email
            user.firstName = email.split('@')[0]
            user.lastName = email.split('@')[0]
            user.phone = email.split('@')[0]
            user.save()


        Cart = cart.objects.filter(user=user)
        if Cart.exists():
            Cart = Cart.first()
        else:
            Cart = cart()
            Cart.user = user
            Cart.save()

        Cart.products.add(product)
        Cart.save()

        return Response(status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def removeItemFromCart(request):
    try:
        prID = request.data['productID']
        product = products.objects.get(pk=int(prID))
        # check if cart exists
        email = request.data['email']
        user = None
        if users.objects.filter(email=email).exists():
            user = users.objects.get(email=email)
        else:
            user = users()
            user.email = email
            user.firstName = email.split('@')[0]
            user.lastName = email.split('@')[0]
            user.phone = email.split('@')[0]
            user.save()

        Cart = cart.objects.filter(user=user)
        if Cart.exists():
            Cart = Cart.first()
        else:
            Cart = cart()
            Cart.user = user
            Cart.save()

        Cart.products.remove(product)
        Cart.save()

        return Response(status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response(status=status.HTTP_400_BAD_REQUEST)

class CartDetail(generics.RetrieveAPIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
    queryset = cart.objects.all()
    serializer_class = CartSerializer

    def get_object(self):
        email = self.kwargs.get('email')
        user = None
        if users.objects.filter(email=email).exists():
            user = users.objects.get(email=email)
        else:
            user = users()
            user.email = email
            user.firstName = email.split('@')[0]
            user.lastName = email.split('@')[0]
            user.phone = email.split('@')[0]
            user.save()
        Cart = cart.objects.filter(user=user)
        if Cart.exists():
            Cart = Cart.first()
        else:
            Cart = cart()
            Cart.user = user
            Cart.save()
        return Cart

class OrderCreate(generics.CreateAPIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
    queryset = order.objects.all()
    serializer_class = CartSerializer

    def create(self, request, *args, **kwargs):
        try:
            email = request.data['email']
            user = None
            if users.objects.filter(email=email).exists():
                user = users.objects.get(email=email)
            else:
                user = users()
                user.email = email
                user.firstName = email.split('@')[0]
                user.lastName = email.split('@')[0]
                user.phone = email.split('@')[0]
                user.save()

            Cart = cart.objects.filter(user=user)
            if Cart.exists():
                Cart = Cart.first()
            else:
                Cart = cart()
                Cart.user = user
                Cart.save()

            newOrder = order()
            newOrder.Customer = user
            idOfProducts = []
            for product in Cart.products.all():
                idOfProducts.append(product.id)

            print(idOfProducts)
            newOrder.totalCost = request.data['totalCost']
            newOrder.fuelStation = fuelStations.objects.get(pk=request.data['fuelStation'])

            newOrder.save()
            newOrder.products.set(idOfProducts)
            newOrder.save()
            Cart.products.clear()
            Cart.save()

            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UnregisteredOrderCreate(generics.CreateAPIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
    queryset = order.objects.all()
    serializer_class = UnregisteredOrderSerializer

    def create(self, request, *args, **kwargs):
        try:
            newOrder = unregisteredOrders()
            email = request.data['email']
            user = None
            if users.objects.filter(email=email).exists():
                user = users.objects.get(email=email)
            else:
                user = users()
                user.email = email
                user.firstName = email.split('@')[0]
                user.lastName = email.split('@')[0]
                user.phone = email.split('@')[0]
                user.save()
            newOrder.Customer = user
            newOrder.totalCost = request.data['totalCost']
            newOrder.station = request.data['station']
            newOrder.description = request.data['description']
            newOrder.serviceType = request.data['serviceType']


            newOrder.save()

            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)


