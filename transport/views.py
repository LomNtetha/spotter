import os
from dotenv import load_dotenv
import datetime
from django.shortcuts import render
from rest_framework import serializers, viewsets
from transport.models import Location, ELDLog, Trip
from . serializers import LocationSerializer,ELDLogSerializer, TripSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
# from .services.services import dijkstra
from django.shortcuts import get_object_or_404
import googlemaps


load_dotenv()

# Initialize Google Maps Client using the API key from .env
gmaps = googlemaps.Client(key=os.getenv('GOOGLE_MAPS_API_KEY'))

class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

class ELDLogViewSet(viewsets.ModelViewSet):
    queryset = ELDLog.objects.all()
    serializer_class = ELDLogSerializer

class TripViewSet(viewsets.ModelViewSet):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer

@api_view(['POST'])
def find_route(request):
    start = request.data.get('start')  # Expecting Location ID
    end = request.data.get('end')

    start_location = get_object_or_404(Location, id=start)
    end_location = get_object_or_404(Location, id=end)

    directions = gmaps.directions(
        (start_location.latitude, start_location.longitude),
        (end_location.latitude, end_location.longitude),
        mode="driving",
        departure_time=datetime.datetime.now()
    )

    if directions:
        route = directions[0]['legs'][0]['steps']
        route_instructions = [step['html_instructions'] for step in route]
        distance = directions[0]['legs'][0]['distance']['text']
        return Response({"route": route_instructions, "distance": distance})
    
    return Response({"error": "No route found."}, status=400)

@api_view(['POST'])
def log_eld_hours(request):
    hours_used = request.data.get('hours_used')
    eld_log = ELDLog.objects.create(hours_used=hours_used)
    return Response({"message": "ELD log added", "log_id": eld_log.id})

@api_view(['GET'])
def get_eld_logs(request):
    logs = ELDLog.objects.order_by('-timestamp')[:5]  # Get last 5 logs
    return Response(ELDLogSerializer(logs, many=True).data)

@api_view(['POST'])
def create_trip(request):
    serializer = TripSerializer(data=request.data)
    if serializer.is_valid():
        trip = serializer.save()
        return Response({"message": "Trip created", "trip_id": trip.id})
    return Response(serializer.errors, status=400)