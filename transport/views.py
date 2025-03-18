import os
from dotenv import load_dotenv
import datetime
from django.shortcuts import render, get_object_or_404
from rest_framework import serializers, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from transport.models import Driver, Location, ELDLog, Trip, Vehicle
from .serializers import DriverSerializer, LocationSerializer, ELDLogSerializer, TripSerializer, VehicleSerializer
import googlemaps

# Load environment variables
load_dotenv()

# Initialize Google Maps Client
google_maps_api_key = os.getenv('GOOGLE_MAPS_API_KEY')
if not google_maps_api_key:
    raise ValueError("Google Maps API key is missing. Please check your .env file.")
gmaps = googlemaps.Client(key=google_maps_api_key)

class DriverViewSet(viewsets.ModelViewSet):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer

class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer

# ViewSets
class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

class ELDLogViewSet(viewsets.ModelViewSet):
    queryset = ELDLog.objects.all()
    serializer_class = ELDLogSerializer

class TripViewSet(viewsets.ModelViewSet):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer

# Custom Views
@api_view(['POST'])
def find_route(request):
    start = request.data.get('start')
    end = request.data.get('end')

    if not start or not end:
        return Response({"error": "Both 'start' and 'end' are required."}, status=400)

    start_location = get_object_or_404(Location, id=start)
    end_location = get_object_or_404(Location, id=end)

    try:
        directions = gmaps.directions(
            (start_location.latitude, start_location.longitude),
            (end_location.latitude, end_location.longitude),
            mode="driving",
            departure_time=datetime.datetime.now()
        )
    except googlemaps.exceptions.ApiError as e:
        return Response({"error": f"Google Maps API error: {str(e)}"}, status=500)

    if directions:
        route = directions[0]['legs'][0]['steps']
        route_instructions = [step['html_instructions'] for step in route]
        distance = directions[0]['legs'][0]['distance']['text']
        return Response({"route": route_instructions, "distance": distance})
    
    return Response({"error": "No route found."}, status=400)

@api_view(['POST'])
def log_eld_hours(request):
    hours_used = request.data.get('hours_used')
    if not hours_used:
        return Response({"error": "'hours_used' is required."}, status=400)

    eld_log = ELDLog.objects.create(hours_used=hours_used)
    return Response({"message": "ELD log added", "log_id": eld_log.id})

@api_view(['GET'])
def get_eld_logs(request):
    logs = ELDLog.objects.order_by('-timestamp')[:5]  # Get last 5 logs
    return Response(ELDLogSerializer(logs, many=True).data)

@api_view(['POST'])
def create_trip(request):
    # Get data from the request
    driver_id = request.data.get('driver_id')
    vehicle_id = request.data.get('vehicle_id')
    trip_hours = request.data.get('trip_hours')
    trip_distance = request.data.get('trip_distance')
    pickup_dropoff_hours = 1  # Additional hour for pickup and drop-off

    # Fetch driver and vehicle
    driver = Driver.objects.get(id=driver_id)
    vehicle = Vehicle.objects.get(id=vehicle_id)

    # Check driver hours
    total_hours = trip_hours + pickup_dropoff_hours
    if not driver.can_drive(total_hours):
        return Response({"error": "Driver cannot work additional hours. A break is required."}, status=400)

    # Check vehicle fueling
    if vehicle.needs_fueling(trip_distance):
        return Response({"error": "Vehicle needs fueling before this trip."}, status=400)

    # Create the trip
    trip = Trip.objects.create(...)

    # Update driver and vehicle
    driver.hours_worked += total_hours
    driver.save()

    vehicle.distance_since_fueling += trip_distance
    vehicle.save()

    return Response({"message": "Trip created", "trip_id": trip.id})