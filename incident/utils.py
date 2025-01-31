import os
from azure.core.exceptions import HttpResponseError
from django.conf import settings
from azure.core.credentials import AzureKeyCredential
from azure.maps.search import MapsSearchClient
from azure.maps.route import MapsRouteClient

subscription_key = settings.AZURE_MAPS_SUBSCRIPTION_KEY

UI_LAT = 7.4418
UI_LON = 3.8964
MAX_RADIUS = 1000  # Max radius in meters

def is_within_university(lat, lon):
    """
    Uses Azure Maps to check if a location is within the University of Ibadan boundary
    by calculating distance from UI's center.
    """
    route_client = MapsRouteClient(credential=AzureKeyCredential(subscription_key))

    try:
        result = route_client.get_route_matrix(
            origins=[(lat, lon)],
            destinations=[(UI_LAT, UI_LON)]
        )

        # Extract distance in meters
        distance_in_meters = result.matrix[0][0].response.route_summary.length_in_meters

        return distance_in_meters <= MAX_RADIUS

    except Exception as e:
        print(f"Azure Maps Route API Error: {e}")
        return False



def geocode(query, value):
    """
    Convert an address into latitude and longitude using Azure Maps.
    """
    maps_search_client = MapsSearchClient(credential=AzureKeyCredential(subscription_key))

    try:
        result = maps_search_client.search_address(query)
        
        if result.results:  # Check if we got results
            position = result.results[0].position  # Get the first result's position
            latitude, longitude = position.lat, position.lon
            
            return latitude if value == "latitude" else longitude if value == "longitude" else None
        else:
            return None

    except Exception as e:
        print(f"Azure Maps Geocoding Error: {e}")
        return None



def reverse_geocode(latitude, longitude):
    """
    Convert latitude and longitude into a human-readable address using Azure Maps.
    """
    maps_search_client = MapsSearchClient(credential=AzureKeyCredential(subscription_key))
    
    try:
        result = maps_search_client.reverse_search_address(coordinate=(latitude, longitude))
        
        if result.addresses:  # Check if we got results
            return result.addresses[0].address.freeform_address  # Get formatted address
        
        return "Address not found"

    except Exception as e:
        print(f"Azure Maps Reverse Geocoding Error: {e}")
        return None
