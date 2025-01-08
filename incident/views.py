from geopy.geocoders import Nominatim
from django.http import JsonResponse
import json
from .models import Incident
from django.shortcuts import render
from .forms import *

# Initialize geolocator
geolocator = Nominatim(user_agent="emergencyapp")

def save_incident(request):
    if request.method == "POST":
        user = request.user
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')

        # Reverse geocode the location
        location = None
        if latitude and longitude:
            location = geolocator.reverse((latitude, longitude), language='en', exactly_one=True)

        # Process the form
        form = IncidentForm(request.POST)
        if form.is_valid():
            # Save the form data
            incident = form.save(commit=False)
            incident.user = user
            if location:
                incident.live_location = location.address  # Save the location address
            incident.save()

            return JsonResponse({'status': 'success', 'message': 'Incident saved successfully'})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'})
