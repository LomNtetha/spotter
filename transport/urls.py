# ------------------------- URLS -------------------------
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from transport.views import DriverViewSet, ELDLogViewSet, LocationViewSet, TripViewSet, VehicleViewSet, create_trip, find_route, get_eld_logs, log_eld_hours

router = DefaultRouter()
router.register(r'locations', LocationViewSet)
router.register(r'eld_logs', ELDLogViewSet)
router.register(r'trips', TripViewSet)
router.register(r'drivers', DriverViewSet)
router.register(r'vehicles', VehicleViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('find_route/', find_route, name='find_route'),
    path('log_eld_hours/', log_eld_hours, name='log_eld_hours'),
    path('get_eld_logs/', get_eld_logs, name='get_eld_logs'),
    path('create_trip/', create_trip, name='create_trip'),
]