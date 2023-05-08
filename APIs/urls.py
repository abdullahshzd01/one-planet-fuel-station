from django.urls import path, register_converter

from django.conf import settings
from django.conf.urls.static import static

from APIs.Views.CartViews import *
from APIs.Views.FuelStationViews import *
from APIs.Views.JobViews import *
from APIs.Views.productViews import *

urlpatterns = [
        path('products/', ProductsList.as_view(), name="products"),
        path('productDetail/<int:pk>/', ProductDetail.as_view(), name="productDetail"),
        path('jobs/', JobsList.as_view(), name="jobs"),
        path('jobDetail/<int:pk>/', JobDetail.as_view(), name="jobDetail"),
        path('jobApply/', ApplicationCreate.as_view(), name="jobApply"),
        path('CartDetail/<str:email>/', CartDetail.as_view(), name="cartDetail"),
        path('fuelstations/', FuelStation.as_view(), name="fuelstations"),
        path('fuelstationDetail/<int:pk>/', FuelStationDetail.as_view(), name="fuelstationDetail"),
        path('addItemToCart/', addItemToCart, name="addItemToCart"),
        path('removeItemFromCart/', removeItemFromCart, name="removeItemFromCart"),
        path('placeOrder/', OrderCreate.as_view(), name="placeOrder"),
        path('placeUnregisteredOrder/', UnregisteredOrderCreate.as_view(), name="placeOrder"),
        path('rateProduct/', ProductRatingCreateUpdate.as_view(), name="rateProduct"),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)