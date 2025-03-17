from django.db import models
from django.shortcuts import get_object_or_404

# ------------------------- Models -------------------------
class Location(models.Model):
    name = models.CharField(max_length=100, unique=True)
    latitude = models.FloatField()
    longitude = models.FloatField()

class ELDLog(models.Model):
    hours_used = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

class Trip(models.Model):
    current_location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='current')
    pickup_location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='pickup')
    dropoff_location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='dropoff')
    cycle_hours_used = models.IntegerField()
    fuel_needed = models.BooleanField(default=False)