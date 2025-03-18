from datetime import timezone
from django.db import models

# ------------------------- Models -------------------------

class Driver(models.Model):
    name = models.CharField(max_length=100)
    hours_worked = models.FloatField(default=0)  # Total hours worked in the current cycle
    last_break = models.DateTimeField(null=True, blank=True)  # Timestamp of the last break

    def can_drive(self, additional_hours):
        """
        Check if the driver can work additional hours without violating HOS rules.
        """
        if self.hours_worked + additional_hours > 70:
            return False
        return True

    def take_break(self):
        """
        Reset the driver's hours after a 34-hour break.
        """
        self.hours_worked = 0
        self.last_break = timezone.now()
        self.save()

class Vehicle(models.Model):
    name = models.CharField(max_length=100)
    distance_since_fueling = models.FloatField(default=0)  # Miles since last fueling

    def needs_fueling(self, additional_distance):
        """
        Check if the vehicle needs fueling after traveling additional_distance miles.
        """
        if self.distance_since_fueling + additional_distance > 1000:
            return True
        return False

    def refuel(self):
        """
        Reset the distance after fueling.
        """
        self.distance_since_fueling = 0
        self.save()
class Location(models.Model):
    """
    Represents a geographical location with a name, latitude, and longitude.
    """
    name = models.CharField(max_length=100, unique=True)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Location"
        verbose_name_plural = "Locations"


class ELDLog(models.Model):
    """
    Represents a log entry for Electronic Logging Device (ELD) hours used.
    """
    hours_used = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"ELD Log {self.id} - {self.hours_used} hours"

    class Meta:
        verbose_name = "ELD Log"
        verbose_name_plural = "ELD Logs"
        ordering = ['-timestamp']  # Order logs by timestamp (newest first)


class Trip(models.Model):
    """
    Represents a trip with a current location, pickup location, dropoff location,
    cycle hours used, and fuel needed status.
    """
    current_location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        related_name='current_trips'
    )
    pickup_location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        related_name='pickup_trips'
    )
    dropoff_location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        related_name='dropoff_trips'
    )
    cycle_hours_used = models.IntegerField()
    fuel_needed = models.BooleanField(default=False)

    def __str__(self):
        return f"Trip {self.id} - {self.current_location.name}"

    class Meta:
        verbose_name = "Trip"
        verbose_name_plural = "Trips"
