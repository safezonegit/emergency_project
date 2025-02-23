import os
import googlemaps
from django.conf import settings
from .models import Incident
from responder.models import *
from twilio.rest import Client
import logging
import requests



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
        # Use 'walking' mode instead of 'driving'
        result = gmaps.distance_matrix(
            origins=[(lat, lon)],
            destinations=[(UI_LAT, UI_LON)],
            mode="walking"  # Change to 'walking'
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
    """
    Sends an SMS notification about an incident to all relevant responders via Termii.
    """
    try:
        incident = Incident.objects.get(incident_id=incident_id)
    except Incident.DoesNotExist:
        print("Incident with id %s not found.", incident_id)
        return

    # Select responders based on incident category
    if incident.category == 'medical':
        responders = MedicalResponder.objects.all()
    elif incident.category == 'fire':
        responders = FireHazardResponder.objects.all()
    elif incident.category == 'security':
        responders = SecurityResponder.objects.all()
    else:
        print("Unknown incident category: %s", incident.category)
        return

    # Construct the SMS message
    message = (
    "URGENT CAMPUS EMERGENCY ALERT!\n\n"
    "Incident Details:\n\n"
    f" Category: {incident.category.upper()}\n"
    f" Severity: {incident.severity.upper()}\n"
    f" Location: {incident.user_input_location or incident.live_location}\n"
    f"Reported By: {incident.user.phone_number}\n\n"

    " IMMEDIATE ACTION REQUIRED! Please mobilize and respond ASAP.\n\n"
    " Powered By SafeZone"
)

    # Termii API configuration from Django settings
    termii_api_url = getattr(settings, "TERMII_API_URL", "https://v3.api.termii.com/api/sms/send")
    termii_api_key = settings.TERMII_API_KEY
    termii_sender_id = settings.TERMII_SENDER_ID

    # Send notification to each responder
    for responder in responders:
        payload = {
            "api_key": termii_api_key,
            "to": format_phone_number(responder.sms_contact),  
            "from": termii_sender_id,
            "sms": message,
            "type": "plain",
            "channel": "generic"
        }
        try:
            response = requests.post(termii_api_url, json=payload, timeout=10)
            response.raise_for_status()
        except requests.HTTPError as exc:
            print("Response Status:", response.status_code)
            print("Response Body:", response.text)
            print("Failed to notify responder %s: %s", responder.name, exc)
        except Exception as exc:
            print("Unexpected error notifying responder %s: %s", responder.name, exc)

