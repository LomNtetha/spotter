from django.contrib import admin
from .models import Location, ELDLog, Trip

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'latitude', 'longitude')
    search_fields = ('name',)

@admin.register(ELDLog)
class ELDLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'hours_used', 'timestamp')
    list_filter = ('timestamp',)
    search_fields = ('hours_used',)

@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ('id', 'current_location', 'pickup_location', 'dropoff_location', 'cycle_hours_used', 'fuel_needed')
    list_filter = ('fuel_needed',)
    search_fields = ('current_location__name', 'pickup_location__name', 'dropoff_location__name')