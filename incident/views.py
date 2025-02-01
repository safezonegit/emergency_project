import googlemaps
from .models import Incident
from django.shortcuts import render,redirect
from .forms import IncidentForm
from .utils import is_within_university,geocode,reverse_geocode
from .tasks import send_incident_notification
import os
from azure.core.exceptions import HttpResponseError
from django.conf import settings
from azure.core.credentials import AzureKeyCredential
from azure.maps.search import MapsSearchClient

subscription_key = settings.AZURE_MAPS_SUBSCRIPTION_KEY


def save_incident(request):
    if request.method == "POST":
        form = IncidentForm(request.POST)
        if form.is_valid():
            user = request.user
            latitude = request.POST.get('latitude')
            longitude = request.POST.get('longitude')
            user_input_location = form.cleaned_data.get('user_input_location')

            live_location = None

            # Validate live location (from geolocation)
            if latitude and longitude:
                try:
                    latitude = float(latitude)
                    longitude = float(longitude)

                    # Reverse geocode the live location
                    live_location = reverse_geocode(latitude, longitude)
                    print(live_location)

                    if not is_within_university(latitude, longitude):
                        form.add_error(None, "Live location is outside the University of Ibadan boundary.")
                        return render(request, 'incident-form.html', {'form': form})
                except ValueError:
                    form.add_error(None, "Invalid location coordinates provided.")
                    return render(request, 'incident-form.html', {'form': form})

            # Validate user input location
            if user_input_location:
                try:
                    input_lat = geocode(user_input_location, "latitude")
                    input_lon = geocode(user_input_location, "longitude")

                    if input_lat is None or input_lon is None:
                        form.add_error('user_input_location', "Unable to geocode the entered location.")
                        return render(request, 'incident-form.html', {'form': form})

                    if not is_within_university(input_lat, input_lon):
                        form.add_error('user_input_location', "The entered location is outside the University of Ibadan boundary.")
                        return render(request, 'incident-form.html', {'form': form})

                except Exception as e:
                    form.add_error('user_input_location', f"Error with location lookup: {e}")
                    return render(request, 'incident-form.html', {'form': form})

            # Save incident if valid
            incident = form.save(commit=False)
            incident.user = user
            incident.live_location = live_location
            incident.save()

            # Send notification asynchronously
            send_incident_notification.delay(incident.incident_id)

            return redirect(request, 'index.html')

    else:
        form = IncidentForm()

    return render(request, 'incident-form.html', {'form': form})

def incident_report_success(request):
    return render(request,'contact.html')