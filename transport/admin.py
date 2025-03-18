from django.contrib import admin
from .models import Driver, Location, ELDLog, Trip, Vehicle

@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ('name', 'hours_worked', 'last_break')  # Fields to display in the admin list view
    search_fields = ('name',)  # Add a search bar for the name field
    list_filter = ('hours_worked',)  # Add filters for the hours_worked field

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('name', 'distance_since_fueling')  # Fields to display in the admin list view
    search_fields = ('name',)  # Add a search bar for the name field
    list_filter = ('distance_since_fueling',)  # Add filters for the distance_since_fueling field

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