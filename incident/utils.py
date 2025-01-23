import googlemaps
from django.conf import settings

gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)

# Define University of Ibadan's center and radius
UI_LAT = 7.4418
UI_LON = 3.8964
MAX_RADIUS = 1000  # Maximum radius in meters

def is_within_university(lat, lon):
    """
    Uses Google Maps API to check if a location is within the University of Ibadan boundary
    by calculating distance from the center of the University of Ibadan.
    """
    try:
        # Geocode the coordinates of the reported location
        distance_result = gmaps.distance_matrix(
            origins=(lat, lon),
            destinations=(UI_LAT, UI_LON),
            mode="driving"
        )
        
        # Extract the distance in meters from the response
        distance_in_meters = distance_result['rows'][0]['elements'][0]['distance']['value']
        
        # Check if the distance is within the specified radius
        return distance_in_meters <= MAX_RADIUS
    except Exception as e:
        print(f"Error with Google Maps API: {e}")
        return False