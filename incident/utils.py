import os
import googlemaps
from django.conf import settings
from .models import Incident
from responder.models import *
from twilio.rest import Client




# Initialize the Google Maps client with your API key
gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)

UI_LAT = 7.4418
UI_LON = 3.8964
MAX_RADIUS = 1000  # Max radius in meters

def is_within_university(lat, lon):
    """
    Check if a location is within the University of Ibadan boundary
    by calculating distance from UI's center using Google Maps Distance Matrix API.
    """
    try:
        # Use Google Maps Distance Matrix API to calculate the distance
        result = gmaps.distance_matrix(
            origins=[(lat, lon)],
            destinations=[(UI_LAT, UI_LON)],
            mode="driving"  # You can also use 'walking', 'bicycling', or 'transit'
        )
        
        # Extract distance in meters
        distance_in_meters = result['rows'][0]['elements'][0]['distance']['value']

        return distance_in_meters <= MAX_RADIUS

    except Exception as e:
        print(f"Google Maps Distance Matrix API Error: {e}")
        return False

def geocode(query, value):
    """
    Convert an address into latitude and longitude using Google Maps Geocoding API.
    """
    try:
        result = gmaps.geocode(query)
        
        if result:  # Check if we got results
            location = result[0]['geometry']['location']  # Get the first result's location
            latitude, longitude = location['lat'], location['lng']
            
            return latitude if value == "latitude" else longitude if value == "longitude" else None
        else:
            return None

    except Exception as e:
        print(f"Google Maps Geocoding Error: {e}")
        return None

def reverse_geocode(latitude, longitude):
    """
    Convert latitude and longitude into a human-readable address using Google Maps Reverse Geocoding API.
    """
    try:
        result = gmaps.reverse_geocode((latitude, longitude))
        
        if result:  # Check if we got results
            return result[0]['formatted_address']  # Get the formatted address
        
        return "Address not found"

    except Exception as e:
        print(f"Google Maps Reverse Geocoding Error: {e}")
        return None



def format_phone_number(phone_number):
    if phone_number.startswith("0"):
        return "+234" + phone_number[1:]  # Replace leading 0 with +234
    elif not phone_number.startswith("+"):
        return "+234" + phone_number  # Ensure it has +234
    return phone_number



def send_incident_notification(incident_id):
    try:
        incident = Incident.objects.get(incident_id=incident_id)
        responders = []

        # Determine responders based on category
        if incident.category == 'medical':
            responders = MedicalResponder.objects.all()
        elif incident.category == 'fire':
            responders = FireHazardResponder.objects.all()
        elif incident.category == 'security':
            responders = SecurityResponder.objects.all()

        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

        for responder in responders:
            message = (
                f"Incident Alert!\n"
                f"Category: {incident.category}\n"
                f"Severity: {incident.severity}\n"
                f"Location: {incident.user_input_location or incident.live_location}\n"
                f"Reported By: {incident.user.username}"
            )
            try:
                formatted_phone = format_phone_number(responder.sms_contact) 
                client.messages.create(
                    to=formatted_phone,
                    from_=settings.TWILIO_PHONE_NUMBER,
                    body=message
                )
            except Exception as e:
                print(f"Failed to notify responder {responder.name}: {e}")
    except Incident.DoesNotExist:
        print("Incident not found.")