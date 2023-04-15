# from django.contrib.auth.backends import ModelBackend
# # from django.contrib.auth import fuelStations
# from .models import fuelStations

# Station = fuelStations()

# class EmailBackend(ModelBackend):
#     def authenticate(self, request, username=None, password=None, **kwargs):
#         try:
#             station = Station.objects.get(email=username)
#         except Station.DoesNotExist:
#             return None

#         if station.check_password(password):
#             return station

#     def get_station(self, station_id):
#         try:
#             return Station.objects.get(pk=station_id)
#         except Station.DoesNotExist:
#             return None
