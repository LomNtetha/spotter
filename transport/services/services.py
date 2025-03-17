import heapq
import math
from models import Location, Road

def dijkstra(start, end):
    """Finds shortest path using Dijkstra's algorithm."""
    locations = {loc.name: loc for loc in Location.objects.all()}
    roads = {loc.name: {} for loc in locations}
    for road in Road.objects.all():
        roads[road.start_location.name][road.end_location.name] = road.distance
        roads[road.end_location.name][road.start_location.name] = road.distance
    
    pq = [(0, start)]
    distances = {loc: float('inf') for loc in roads}
    distances[start] = 0
    previous = {}
    
    while pq:
        curr_dist, curr_loc = heapq.heappop(pq)
        if curr_loc == end:
            return reconstruct_path(previous, start, end), curr_dist
        
        for neighbor, weight in roads[curr_loc].items():
            distance = curr_dist + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous[neighbor] = curr_loc
                heapq.heappush(pq, (distance, neighbor))
    
    return None, float('inf')

def reconstruct_path(previous, start, end):
    """Reconstructs shortest path from start to end."""
    path = []
    current = end
    while current in previous:
        path.append(current)
        current = previous[current]
    path.append(start)
    return path[::-1]

def haversine_distance(loc1, loc2):
    """Computes distance using latitude and longitude."""
    R = 6371
    dlat = math.radians(loc2.latitude - loc1.latitude)
    dlon = math.radians(loc2.longitude - loc1.longitude)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(loc1.latitude)) * math.cos(math.radians(loc2.latitude)) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c